import subprocess
import os
import signal
import time

class SoundPlayer:
    def __init__(self, python_path="C:/Users/VICON/Desktop/Code/psychopyMuseum/psychopyMuseum/psychopy_env/Scripts/python.exe"):
        self.process = None
        self.python_path = python_path

    def play(self, sound_path=None):
        if self.process is not None:
            print("Sound is already playing.")
            return
        self.process = subprocess.Popen([self.python_path, "-c", f"from playsound import playsound; playsound(r'{sound_path}')"])

    def stop(self):
        if self.process is not None:
            os.kill(self.process.pid, signal.SIGTERM)
            self.process = None
        else:
            print("No sound is playing.")

# Example usage:
# player = SoundPlayer()
# player.play(r"C:\Users\VICON\Desktop\Code\psychopyMuseum\psychopyMuseum\noise_folder\background_noise_30.wav")
# time.sleep(2)
# player.stop()
# time.sleep(1)
# player.play(r"C:\Users\VICON\Desktop\Code\psychopyMuseum\psychopyMuseum\noise_folder\background_noise_30.wav")
# time.sleep(2)
# player.stop()
