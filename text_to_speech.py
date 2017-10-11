import platform
import requests
import subprocess
import tempfile

try:
    from gtts import gTTS
    from pygame import mixer
    mixer.init()
except ImportError:
    pass


system = platform.system()


def say(text):
    if system == 'Linux':
        try:
            with tempfile.NamedTemporaryFile() as f:
                gTTS(text).save(f.name)
                mixer.music.load(f.name)
                mixer.music.play()
        except (NameError, requests.ConnectionError):
            subprocess.Popen(['espeak', text]).wait()
    elif system == 'Darwin':
        subprocess.Popen(['say', text]).wait()
    else:
        raise NotImplementedError
