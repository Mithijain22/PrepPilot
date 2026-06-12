import whisper
import sounddevice as sd
import soundfile as sf
import os

model = whisper.load_model("base")

TEMP_DIR = os.path.abspath("assets/temp_audio")  # ✅ Absolute path

def ensure_dir():
    os.makedirs(TEMP_DIR, exist_ok=True)

def record_audio(duration=10, sample_rate=16000, filename="input.wav"):
    ensure_dir()
    filepath = os.path.join(TEMP_DIR, filename)
    
    print(f"🎙️ Recording... saving to {filepath}")
    audio = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype='float32'
    )
    sd.wait()
    sf.write(filepath, audio, sample_rate)
    print(f"✅ File saved: {os.path.exists(filepath)}")  # True aana chahiye
    return filepath

def transcribe_audio(filepath):
    filepath = os.path.abspath(filepath)  # ✅ Always absolute
    print(f"📝 Transcribing: {filepath}")
    print(f"📁 File exists: {os.path.exists(filepath)}")
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Audio file not found: {filepath}")
    
    result = model.transcribe(filepath)
    text = result["text"].strip()
    print(f"✅ Transcribed: {text}")
    return text