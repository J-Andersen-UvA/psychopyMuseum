import asyncio
import websockets
import time

class WebSocketClient:
    def __init__(self, host, port):
        self.uri = f"ws://{host}:{port}"

    async def __send_message(self, message):
        async with websockets.connect(self.uri) as websocket:
            await websocket.send(message)
            print(f"Sent message: {message}")

    async def send_name(self, name):
        await self.__send_message(f"SetName {name}")
    
    async def send_start_record(self):
        await self.__send_message("Start")
    
    async def send_stop_record(self):
        await self.__send_message("Stop")

    async def send_kill(self):
        await self.__send_message("Kill")

    async def request_file(self, ip, port):
        await self.__send_message(f"SendFilePrevious {ip} {port}")

# Example usage
if __name__ == "__main__":
    # Start the file receiver in a new terminal (uses the python interpreter from the psychopy environment and the receiver script)
    from OBSRecorder.src.src_sendAndReceive.receiveFiles import AsyncFileReceiver, run_receiver_in_new_terminal
    run_receiver_in_new_terminal("192.168.0.180", 4422, "./output", python_path="C:/Users/VICON/Desktop/Code/psychopyMuseum/psychopyMuseum/psychopy_env/Scripts/python.exe", receiver_script_path="C:/Users/VICON/Desktop/Code/psychopyMuseum/psychopyMuseum/src/OBSRecorder/src/src_sendAndReceive/receiveFiles.py")

    # Start the client
    client = WebSocketClient("192.168.0.211", 4422)
    asyncio.run(client.send_name("NameRecording"))
    asyncio.run(client.send_start_record())
    # Wait 2 seconds for recording to finish
    time.sleep(2)
    asyncio.run(client.send_stop_record())

    # Request the file to be sent, use the same IP and port as the receiver
    asyncio.run(client.request_file("192.168.0.180", 4422))

