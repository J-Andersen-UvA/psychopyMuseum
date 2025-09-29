"""
File: LiveLinkFace.py

Description:
This file defines the LiveLinkFaceClient and LiveLinkFaceServer classes for
communicating with two iPhone servers via OSC (Open Sound Control) protocol.

Classes:
- LiveLinkFaceClient: Sends messages to the iPhone Live Link server.
- LiveLinkFaceServer: Launches the Live Link server and communicates with the iPhone.

LiveLinkFaceClient:
- The __init__ method initializes the client and sets the Python server address on the iPhone.
- The start_capture method instructs the iPhone to start capturing.
- The stop_capture method instructs the iPhone to stop capturing.
- The set_filename method sets the file name for capturing.
- The request_battery method requests the battery status from the iPhone.
- The save_file method sends a transport message to the iPhone to save a file.

LiveLinkFaceServer:
- The __init__ method initializes the server and client objects for communication with the iPhone.
- The init_server method starts the server to receive messages from the iPhone.
- The quit_server method exits the server and client.
- The start_recording method starts recording with the iPhone and TCP socket.
- The send_close_tcp method sends a close command to the TCP socket.
- The send_file_name_tcp method sends a file name to the TCP socket.
- The send_are_you_okay_tcp method checks if the TCP socket is okay.
- The send_signal_recording_tcp method sets the TCP socket to file receiving mode.
- The ping_back method responds to requests, indicating that the OSC server is alive.
- The default method prints all received messages by default.
"""
from pythonosc.udp_client import SimpleUDPClient
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from fileReceiver import FileReceiver
import sys
import socket


def get_local_ip_for_dest(dest_ip):
    """
    Opens a dummy UDP socket to dest_ip and reads back the local side address.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # port number doesn’t matter since we won't actually send anything
        s.connect((dest_ip, 1))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = None
    finally:
        s.close()
    return local_ip

class LiveLinkFaceClient:
    """
    Class LiveLinkFaceClient sends messages to the live link server on the iPhone.

    Methods:
    - __init__: Initializes the client and sets the Python server address on the iPhone.
    - start_capture: Sends a message to start capturing to the iPhone server.
    - stop_capture: Sends a message to stop capturing to the iPhone server.
    - set_filename: Sets the file name for capturing on the iPhone server.
    - request_battery: Requests battery information from the iPhone server.
    - save_file: Sends a transport message to the iPhone for saving a file.

    Attributes:
    - toIphone: SimpleUDPClient instance for communication with the iPhone server.
    - gloss: Current gloss set for capturing.
    - args: Arguments for configuring the client.
    """

    def __init__(self, args, gloss, ip_iphone):
        """
        Initialize the LiveLinkFaceClient.

        Args:
        - args: The arguments containing necessary configurations.
        - gloss: The initial gloss for capturing.

        Description:
        This method initializes the LiveLinkFaceClient instance. It sets up the UDP client
        for communication with the iPhone server, sets the Python server address on the iPhone,
        and initializes other necessary attributes.
        """
        self.ip_iphone = ip_iphone
        self.port = args.get('llf_port', None)
        self.ip_machine = get_local_ip_for_dest(ip_iphone)
        
        self.phone_present = False
        self.phone_handshake = False
        self.record_stop_confirm = True

        self.gloss = gloss
        self.args = args
        self.takenumber = 0

        
        if not self.ip_iphone or not self.port:
            print("[LLF Error] Missing iPhone IP or llf_port in args")
        else:
            self.init_apple_con()
        
        # Set gloss of first sign
        self.set_filename(self.gloss)
    
    def init_apple_con(self):

        if self.phone_present:
            return

        print(f"[LLF] Phone initialized, sending to {self.ip_iphone}:{self.port}")
        self.toIphone = SimpleUDPClient(self.ip_iphone, self.port)
        self.phone_present = True

        self.send_message_to_iphone("/OSCSetSendTarget", [self.ip_machine, self.port])
        self.send_message_to_iphone("/VideoDisplayOn", [])

    def send_message_to_iphone(self, msg, *args):
        """Send OSC message to the iPhone."""
        if not self.phone_present:
            print("[LLF Warning] iPhone connection not initialized.")
            return
        print(f"[LLF] Sending msg {msg} with args {args}")
        self.toIphone.send_message(msg, *args)

    def start_capture(self, *args):
        """
        Start capturing on the iPhone server.

        Returns:
        The current capture number.

        Description:
        This method sends a message to the iPhone server to start capturing.
        It increments the capture number and returns it.
        """
        self.send_message_to_iphone("/RecordStart", [self.gloss, self.takenumber])
        return self.takenumber

    def stop_capture(self, *args):
        """
        Stop capturing on the iPhone server.

        Description:
        This method sends a message to the iPhone server to stop capturing.
        It also increments the capture number.
        """
        self.send_message_to_iphone("/RecordStop", [])
        self.takenumber += 1
        self.record_stop_confirm = False

    def set_filename(self, gloss, *args):
        """
        Set the file name for capturing on the iPhone server.

        Args:
        - gloss: The gloss to be set as the file name.

        Description:
        This method sets the file name for capturing on the iPhone server.
        It also resets the capture number.
        """
        print("Setting filename to: ", gloss)

        # Don't reset the take number if the gloss is the same
        if self.gloss != gloss:
            self.takenumber = 0

        self.gloss = gloss
        self.send_message_to_iphone("/Slate", [self.gloss])
    
    def request_battery(self, *args):
        """
        Request battery information from the iPhone server.

        Description:
        This method sends a message to the iPhone server to request battery information.
        """
        self.send_message_to_iphone("/BatteryQuery", [])

    def video_display_on(self, *args):
        """
        Notify the iPhone server that the video display is on.

        Description:
        This method sends a message to the iPhone server to indicate that the video display is on.
        """
        self.send_message_to_iphone("/VideoDisplayOn", [])
    
    def video_display_off(self, *args):
        """
        Notify the iPhone server that the video display is off.

        Description:
        This method sends a message to the iPhone server to indicate that the video display is off.
        """
        self.send_message_to_iphone("/VideoDisplayOff", [])

    def save_file(self, command, timecode, blendshapeCSV, referenceMOV, *args):
        """
        Save a file on the iPhone server.

        Args:
        - timecode: Timecode information.
        - blendshapeCSV: Blendshape CSV data.
        - referenceMOV: Reference MOV file.

        Description:
        This method sends a transport message to the iPhone server to save a file.
        """
        print(f"[LLF] Saving file with command: {command}, timecode: {timecode}, blendshapeCSV: {blendshapeCSV}, referenceMOV: {referenceMOV}")
        self.record_stop_confirm = True
        # File name has the format 20250714_test7_250714_5_0/test7_250714_5_0_vislabLivelink_cal.csv so lets remove the first part
        splitBlendshapeCSV = blendshapeCSV.split("/")[-1]
        splitReferenceMOV = referenceMOV.split("/")[-1]
        csv_receiver = FileReceiver(host=self.ip_machine, port=self.args.get('receive_csv_port', None), output_dir=self.args.get('llf_save_path_csv', None), filename=splitBlendshapeCSV, endpoint=self.args.get('endpoint', 'https://signcollect.nl/razerUpload/upload.php'), send_to_endpoint=True)
        mov_receiver = FileReceiver(host=self.ip_machine, port=self.args.get('receive_video_port', None), output_dir=self.args.get('llf_save_path_video', None), filename=splitReferenceMOV, endpoint=self.args.get('endpoint', 'https://signcollect.nl/razerUpload/upload.php'), send_to_endpoint=True)
        print(f"send the transport towards:\tCSV{self.ip_machine,}:{str(self.args.get('receive_csv_port', None))}\tMOV{IP_MACHINE}:{str(self.args.get('receive_video_port', None))}")
        self.send_message_to_iphone("/Transport", [f"{self.ip_machine}:{csv_receiver.port}", blendshapeCSV])
        self.send_message_to_iphone("/Transport", [f"{self.ip_machine}:{mov_receiver.port}", referenceMOV])

class LiveLinkFaceServer: 
    """
    Class LiveLinkFaceServer launches the live link server that communicates with the iPhone.

    Description:
    The IP used in this server should be the same as the listener in the iPhone.
    The server is NOT launched asynchronously, but it contains the client object to do any communication
    to the iPhone where necessary.
    The server is a man in the middle for all the communication with the iPhone, including setting up the
    TCP connection for the file transfer.
    """
    def __init__(self, gloss, args, iphone_ips):
        """
        Initialize the LiveLinkFaceServer.

        Args:
        - gloss: The gloss for capturing.
        - args: The arguments containing necessary configurations.

        Description:
        This method initializes the LiveLinkFaceServer instance. It sets up the dispatcher for handling
        incoming messages, initializes the client object, and sets up rules for message handling.
        """
        self.gloss = gloss
        self.args = args
        self.clients = {ip: LiveLinkFaceClient(args, gloss, ip) for ip in iphone_ips}
        # status tracking per iPhone
        self.battery_percentage = {ip: 100.0 for ip in iphone_ips}
        self.dispatcher = Dispatcher()

        # OSC mappings
        self.dispatcher.map("/OSCSetSendTargetConfirm", self.set_target_confirmed)
        self.dispatcher.map("/QuitServer", self.quit_server)
        self.dispatcher.map("/RecordStart", self.start_recording)
        self.dispatcher.map("/RecordStop", self.stop_recording)
        self.dispatcher.map("/SetFileName", self.set_filename)
        self.dispatcher.map("/RecordStopConfirm", self.save_file)
        self.dispatcher.map("/BatteryQuery", self.request_battery)
        self.dispatcher.map("/Battery", self.update_battery)
        self.dispatcher.set_default_handler(self.default)

    def init_server(self):
        self.ip_machine = "0.0.0.0"  # listen on all interfaces
        print("Receiving iPhone On: ", self.ip_machine, self.args.get('llf_port'))
        self.server = BlockingOSCUDPServer((self.ip_machine, self.args.get('llf_port')), self.dispatcher)
        self.server.serve_forever()

    # -------------------
    # Dispatcher handlers
    # -------------------
    def start_recording(self, addr, iphone_ip=None, *args):
        if iphone_ip and iphone_ip in self.clients:
            self.clients[iphone_ip].start_capture()
        else:
            for client in self.clients.values():
                client.start_capture()

    def stop_recording(self, addr, iphone_ip=None, *args):
        if iphone_ip and iphone_ip in self.clients:
            self.clients[iphone_ip].stop_capture()
        else:
            for client in self.clients.values():
                client.stop_capture()

    # per round
    def start_recording_round(self, round_gloss):
        """
        Start recording on all iPhones for a specific round.
        Args:
            round_gloss: string, used as filename/label for the round
        """
        print(f"[LLF] Starting round recording: {round_gloss}")
        for client in self.clients.values():
            client.set_filename(round_gloss)
            client.start_capture()

    def stop_recording_round(self):
        """
        Stop recording on all iPhones for the current round.
        """
        print(f"[LLF] Stopping round recording")
        for client in self.clients.values():
            client.stop_capture()

    def set_filename(self, addr, file_name, iphone_ip=None, *args):
        if iphone_ip and iphone_ip in self.clients:
            self.clients[iphone_ip].set_filename(file_name)
        else:
            for client in self.clients.values():
                client.set_filename(file_name)

    def save_file(self, addr, command, timecode, blendshapeCSV, referenceMOV, iphone_ip=None, *args):
        if iphone_ip and iphone_ip in self.clients:
            self.clients[iphone_ip].save_file(command, timecode, blendshapeCSV, referenceMOV)
        else:
            for client in self.clients.values():
                client.save_file(command, timecode, blendshapeCSV, referenceMOV)

    def request_battery(self, addr, iphone_ip=None, *args):
        if iphone_ip and iphone_ip in self.clients:
            self.clients[iphone_ip].request_battery()
        else:
            for client in self.clients.values():
                client.request_battery()

    def update_battery(self, addr, iphone_ip, flt, *args):
        if iphone_ip in self.battery_percentage:
            self.battery_percentage[iphone_ip] = flt * 100.0

    def set_target_confirmed(self, addr, iphone_ip, *args):
        if iphone_ip in self.clients:
            self.clients[iphone_ip].phone_handshake = True
            print(f"[LLF] Target confirmed by iPhone {iphone_ip}")

    def video_display_on(self, addr, iphone_ip, *args):
        if iphone_ip in self.clients:
            print(f"[LLF] Video display on confirmed by iPhone {iphone_ip}")
            self.clients[iphone_ip].video_display_on()

    def video_display_off(self, addr, iphone_ip, *args):
        if iphone_ip in self.clients:
            print(f"[LLF] Video display off confirmed by iPhone {iphone_ip}")
            self.clients[iphone_ip].video_display_off()

    # -------------------
    # Utilities
    # -------------------
    def quit_server(self, *args):
        sys.exit()

    def default(self, address, *args):
        print(f"{address}: {args}")

    def health_check(self, debug=False):
        for ip, client in self.clients.items():
            if not client.phone_present:
                if debug: print(f"[LLF Warning] iPhone {ip} not present.")
                return False, f"iPhone {ip} not present"
            if not client.phone_handshake:
                if debug: print(f"[LLF Warning] iPhone {ip} handshake not confirmed.")
                return False, f"iPhone {ip} handshake not confirmed"
            if not client.record_stop_confirm:
                if debug: print(f"[LLF Warning] iPhone {ip} record stop not confirmed.")
                return False, f"iPhone {ip} record stop not confirmed"
            if self.battery_percentage[ip] < 11:
                if debug: print(f"[LLF Warning] iPhone {ip} battery low: {self.battery_percentage[ip]}%")
                return False, f"iPhone {ip} battery low"
        return True, ""

    def stop_server(self):
        try:
            if hasattr(self, 'server') and self.server:
                self.server.server_close()
        except Exception as e:
            print(f"[Warning] Exception while stopping OSC server: {e}")
