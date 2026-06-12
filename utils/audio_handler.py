import os
import sounddevice as sd
import soundfile as sf

TEMP_DIR = "assets/temp_audio"

def ensure_temp_dir():
    os.makedirs(TEMP_DIR, exist_ok=True)

def save_audio(audio_data, sample_rate=16000, filename="input.wav"):
    ensure_temp_dir()
    path = os.path.join(TEMP_DIR, filename)
    sf.write(path, audio_data, sample_rate)
    return path

def delete_audio(filename):
    path = os.path.join(TEMP_DIR, filename)
    if os.path.exists(path):
        os.remove(path)

def list_temp_files():
    return os.listdir(TEMP_DIR)