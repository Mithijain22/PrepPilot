from dotenv import load_dotenv
import os

load_dotenv()

HF_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Model config
DEFAULT_MODEL = "mistralai/Mistral-7B-Instruct-v0.1"
LIGHTWEIGHT_MODEL = "google/flan-t5-base"  # for low-end PCs

# Audio config
RECORDING_DURATION = 10
SAMPLE_RATE = 16000

# Interview config
MAX_QUESTIONS = 10