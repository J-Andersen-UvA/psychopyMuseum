import yaml
import os
import helpers.popUp as popUp
from OBSRecorder.src.src_sendAndReceive.receiveFiles import run_receiver_in_new_terminal
import OBSRecorder.src.obsRecording as obsRecording
from audioPlayerPy.PyAudioPlayer import PyAudioPlayer as AudioPlayer
import websockets

popUp = popUp.PopUp()

class ExperimentSetup:
    """
    This is a setup class to fetch the default variables from.
    """
    def __init__(self, config_file="config.yaml"):
        self.config = None
        # Load the YAML configuration file
        with open(config_file, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Parse config into attributes
        self.experiment_name = self.config["experiment"]["name"]
        self.author = self.config["experiment"]["author"]
        self.description = self.config["experiment"]["description"]

        # Window configuration
        self.window_size = self.config["window"]["size"]
        self.window_color = self.config["window"]["color"]
        self.window_units = self.config["window"]["units"]
        self.fullscreen = self.config["window"]["fullscreen"]

        # windows assigned to screens
        self.screenA = self.config["winA"]
        self.screenB = self.config["winB"]

        # File paths
        self.output_folder = os.path.abspath(self.config["files"]["output_folder"])
        self.noise_soc, self.noise_soc_volume = self.config["files"]["noise_soc"]
        self.noise_nonsoc, self.noise_nonsoc_volume = self.config["files"]["noise_nonsoc"]

        # Keyboard
        # self.key_1 = self.config["input"]["key_1"]
        # self.key_2 = self.config["input"]["key_2"]
        # self.key_3 = self.config["input"]["key_3"]
        # self.key_4 = self.config["input"]["key_4"]
        self.allowed_keys = {}
        for i, key in enumerate(self.config["input"], start=0):
            self.allowed_keys[self.config["input"][key]] = i

        print(f"[GEN SETUP] self.allowed_keys:{self.allowed_keys}")

        # Timing
        self.intro_duration = self.config["timing"]["intro_duration"]
        self.instructions_duration = self.config["timing"]["instructions_duration"]
        self.description_duration = self.config["timing"]["description_duration"]

        self.python_path = self.config["python_path"]

        # OBS connection setup
        self.no_obs = self.config["no_obs"]
        if not self.no_obs:
            self.obs = self.OBSConnection(self.config)
        
        # Audio player
        self.audio_player = AudioPlayer()

    class OBSConnection:
        def __init__(self, config):
            # self.receiver_machine_ip = config["receiver_machine"]["ip"]
            # self.receiver_machine_port = config["receiver_machine"]["port"]
            # self.python_path = config["python_path"]
            # self.receiver_script_path = config["receiver_script_path"]
            self.output_folder = os.path.abspath(config["files"]["output_folder"])
            # run_receiver_in_new_terminal(self.receiver_machine_ip, self.receiver_machine_port, self.output_folder + "\\video", self.receiver_script_path, self.python_path)

            self.obs_target_host = config["obs_host"]["target_host"]
            self.obs_target_port = config["obs_host"]["target_port"]
            # self.obs_ws = f"ws://{self.obs_target_host}:{self.obs_target_port}"
            self.obs = obsRecording.OBSController(self.obs_target_host, self.obs_target_port, None, popUp=popUp)
            self.obs.set_record_directory(self.output_folder)
            self.obs.set_buffer_folder(config["files"]["obs_buffer_folder"])

        async def send_message_obs(self, message):
            async with websockets.connect(self.obs_ws) as websocket:
                await websocket.send(message)
                print(f"Sent message: {message}")

        def send_name_obs(self, name):
            self.obs.set_save_location(self.output_folder, name)
            # await self.send_message_obs(f"SetName {name}")

        def send_start_record_obs(self):
            self.obs.start_recording()
            # await self.send_message_obs("Start")

        def send_stop_record_obs(self):
            self.obs.stop_recording()
            # await self.send_message_obs("Stop")

        async def send_request_file_obs(self):
            await self.send_message_obs(f"SendFilePrevious {self.receiver_machine_ip} {self.receiver_machine_port}")

    def validate_paths(self):
        """
        Ensure required files and directories exist
        """
        files_to_check = [
            self.noise_soc,
            self.noise_nonsoc
        ]

        # Check if the root folder exists
        if not os.path.exists(self.output_folder):
            create = popUp.show_popup_yesno(
                "Warning", f"The output folder '{self.output_folder}' does not exist. Do you want to create it?"
            )
            if not create:
                raise ValueError(f"Output folder path '{self.output_folder}' does not exist.")
            else:
                os.makedirs(self.output_folder, exist_ok=True)

        # Check if the main files exist
        for file in files_to_check:
            if not os.path.exists(file):
                popUp.show_warning_then_exit(
                    "Warning", f"The file '{file}' does not exist. Quiting the program..."
                )

        # # Check if the image folder exists
        # if not os.path.exists(self.img_folder):
        #     create = popUp.show_popup_yesno(
        #         "Warning", f"The image folder '{self.img_folder}' does not exist. Do you want to create it?"
        #     )
        #     if not create:
        #         raise FileNotFoundError(f"Image folder not found: {self.img_folder}")
        #     else:
        #         os.makedirs(self.img_folder, exist_ok=True)
