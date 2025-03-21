import pyaudio
import wave
import threading
import time

class PyAudioPlayer:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.wf = None
        self.is_paused = False
        self.is_playing = False
        self.stop_playback = False
        self.audio_thread = None
        self.current_audio = None

    def _play_audio(self):
        """Internal method to handle audio playback."""
        chunk = 1024
        self.stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                                  channels=self.wf.getnchannels(),
                                  rate=self.wf.getframerate(),
                                  output=True)
        while not self.stop_playback:
            if self.is_paused:
                time.sleep(0.1)  # Pause without consuming CPU
                continue
            data = self.wf.readframes(chunk)
            if not data:
                break
            self.stream.write(data)
        self._cleanup()

    def _cleanup(self):
        """Stops and closes the audio stream."""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        if self.wf:
            self.wf.close()
            self.wf = None
        self.is_playing = False

    def play(self, path_to_audio=None):
        """Play or resume audio. If a path is given, play from the beginning."""
        if path_to_audio:
            if self.is_playing:
                self.stop()
            self.current_audio = path_to_audio
            self.wf = wave.open(path_to_audio, 'rb')
            self.stop_playback = False
            self.is_paused = False
            self.is_playing = True
            self.audio_thread = threading.Thread(target=self._play_audio, daemon=True)
            self.audio_thread.start()
        elif self.is_playing and self.is_paused:
            self.is_paused = False  # Resume playback
        else:
            print("No audio to play or resume.")

    def isPlaying(self):
        return self.is_playing

    def pause(self):
        """Pause the currently playing audio."""
        if self.is_playing:
            self.is_paused = True
        else:
            print("No audio playing.")

    def stop(self):
        """Stop the audio completely."""
        if self.is_playing:
            self.stop_playback = True
            if self.audio_thread:
                self.audio_thread.join()  # Ensure playback thread stops
        else:
            print("No audio playing.")

    def __del__(self):
        """Cleanup PyAudio instance when the object is deleted."""
        if self.p:
            self.p.terminate()

# Example Usage:
# player = PyAudioPlayer()
# player.play("./example_audio/background_noise_10.wav")
# time.sleep(2)
# player.pause()
# time.sleep(2)
# player.play()
# time.sleep(2)
# player.stop()