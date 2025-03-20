import subprocess
import os
import signal
import time
import threading
from playsound import playsound

class SoundPlayer:
    def __init__(self, python_path="C:/Users/VICON/Desktop/Code/psychopyMuseum/psychopyMuseum/psychopy_env/Scripts/python.exe"):
        self.process = None
        self.python_path = python_path

    def play(self, sound_path=None):
        if self.process is not None:
            print("Sound is already playing.")
            return

        if os.path.exists(sound_path):
            print(f"Sound file exists: {sound_path}.")
        else:
            print(f"Sound file does NOT exist {sound_path}.")

        def play_sound():
            cmd = f"""from playsound import playsound; playsound(r"{sound_path}")"""
            print(cmd)
            self.process = subprocess.Popen(
                [self.python_path, "-c", cmd],
                creationflags=subprocess.CREATE_NO_WINDOW  # No visible terminal
            )

        # self.process = threading.Thread(target=play_sound)
        # self.process.start()

        play_sound()

        print("Sound started.")

    def stop(self):
        if self.process is not None:
            self.process.terminate()  # Gracefully terminates the process
            self.process = None
        else:
            print("No sound is playing.")

# Example usage:
# player = SoundPlayer()
# # player.play(r"C:\\Users\\VICON\\Desktop\\Code\\psychopyMuseum\\psychopyMuseum\\noise_folder\\background_noise_30.wav")
# # time.sleep(2)
# # player.stop()
# # time.sleep(1)
# player.play("C:\\Users\\VICON\\Desktop\\Code\\psychopyMuseum\\psychopyMuseum\\noise_folder\\background_noise_30.wav")
# time.sleep(2)
# player.stop()
