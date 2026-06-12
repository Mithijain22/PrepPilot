# 🎙️ AI Voice Interviewer

An AI-powered voice-based mock interview platform that conducts dynamic, company-specific interviews using speech recognition and text-to-speech. Practice real interviews with adaptive follow-up questions powered by Groq LLM.

---

## 🚀 Features

- 🎤 **Voice Input** — Record your answers using microphone (Whisper STT)
- 🔊 **Voice Output** — Interviewer speaks questions aloud (gTTS)
- 🤖 **AI-Generated Questions** — Dynamic questions via Groq LLM (no hardcoded JSON)
- 🏢 **50+ Companies** — Google, Amazon, Microsoft, Flipkart, Zomato, Razorpay and more
- 💼 **Multiple Roles** — SDE, Data Scientist, ML Engineer, Backend, Frontend, DevOps
- 📊 **3 Difficulty Levels** — Easy, Medium, Hard
- 🔄 **Adaptive Follow-ups** — AI asks follow-up based on your actual answer
- 📝 **Detailed Feedback** — Score, strengths, weaknesses, and final verdict
- ⌨️ **Text Fallback** — Type answers if mic not available

---

## 🗂️ Project Structure

```
ai-voice-interviewer/
├── app.py                        # Main Streamlit app
├── config.py                     # Settings and env loader
├── requirements.txt
├── .env                          # API keys (not committed)
│
├── core/
│   ├── __init__.py
│   ├── stt.py                   # Speech-to-Text (Whisper)
│   ├── tts.py                   # Text-to-Speech (gTTS + pygame)
│   ├── interview_engine.py      # Adaptive interview logic
│   └── question_generator.py   # Groq API question generation
│
├── utils/
│   ├── audio_handler.py         # Audio file management
│   └── context_tracker.py      # Conversation history tracker
│
├── data/
│   ├── companies/               # (Optional) company JSON data
│   └── roles/                   # (Optional) role JSON data
│
└── assets/
    └── temp_audio/              # Temporary audio files
```

---

## 🛠️ Tech Stack

| Category | Technology |
|---|---|
| Frontend | Streamlit |
| Speech-to-Text | OpenAI Whisper |
| Text-to-Speech | gTTS + pygame |
| LLM | Groq API (LLaMA 3.1) |
| Audio Recording | sounddevice + soundfile |
| Environment | python-dotenv |

---

## ⚙️ Installation

### Prerequisites
- Python 3.10+
- FFmpeg installed and added to PATH
- Microphone (for voice input)
- Internet connection (for gTTS and Groq API)

### Step 1 — Clone / Setup Project
```bash
git clone https://github.com/your-username/ai-voice-interviewer.git
cd ai-voice-interviewer
```

### Step 2 — Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### Step 3 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Install FFmpeg (Windows)
Download from: https://www.gyan.dev/ffmpeg/builds/

Extract to `C:\ffmpeg\` and add `C:\ffmpeg\bin` to System PATH.

Verify:
```bash
ffmpeg -version
```

### Step 5 — Setup API Keys
Create `.env` file in root folder:
```env
GROQ_API_KEY=your_groq_api_key_here
HUGGINGFACEHUB_API_TOKEN=your_hf_token_here
```

Get Groq API key free at: https://console.groq.com

### Step 6 — Run the App
```bash
streamlit run app.py
```

---

## 🎯 How to Use

```
1. Open http://localhost:8501 in browser
       ↓
2. Select Company, Role, Difficulty from sidebar
       ↓
3. Click "Start Interview"
       ↓
4. AI generates and speaks a question
       ↓
5. Click "Record" to answer via voice (or type)
       ↓
6. AI transcribes → generates smart follow-up
       ↓
7. Repeat for multiple rounds
       ↓
8. Click "End Interview" → get detailed feedback
```

---

## 🏢 Supported Companies

### 🇺🇸 Big Tech (FAANG+)
Google, Amazon, Microsoft, Meta, Apple, Netflix, LinkedIn, Uber, Airbnb, Twitter/X

### 🇺🇸 US Tech
Salesforce, Adobe, Oracle, IBM, Nvidia, Stripe, Dropbox, Snowflake, OpenAI, Anthropic, Spotify, PayPal

### 🇮🇳 Indian Tech
Flipkart, Zomato, Swiggy, Ola, Paytm, CRED, Razorpay, Freshworks, Zoho, PhonePe, Meesho, Zerodha, Groww, Dream11

### 🌏 Global
Samsung, Sony, Accenture, Capgemini, Cognizant

---

## 💼 Supported Roles

- Software Development Engineer (SDE)
- Data Scientist
- ML Engineer
- Backend Developer
- Frontend Developer
- DevOps Engineer

---

## 📊 Feedback Format

At the end of each interview, AI provides:

```
1. Overall Score       : X/10
2. Technical Skills    : X/10
3. Communication       : X/10
4. Strengths           : 3 bullet points
5. Areas to Improve    : 3 bullet points
6. Final Verdict       : Hire / Strong Maybe / Maybe / No Hire
7. Advice              : One line tip for candidate
```

---

## 📦 requirements.txt

```txt
streamlit
openai-whisper
gtts
groq
langchain
langchain-community
transformers
torch
huggingface_hub
sounddevice
soundfile
numpy
python-dotenv
pygame
accelerate
```

---

## ⚠️ Common Issues & Fixes

| Error | Fix |
|---|---|
| `WinError 2` during transcription | FFmpeg not installed or not in PATH |
| `model_decommissioned` Groq error | Update model name to `llama-3.1-8b-instant` |
| `No module named 'groq'` | Run `pip install groq` |
| `Microphone not found` | Check sounddevice installation |
| `TTS not working` | Check internet connection (gTTS needs internet) |
| `accelerate` error | Run `pip install accelerate` |
| Whisper slow on CPU | Normal — wait 30-60 seconds for transcription |

---

## 🔮 Future Improvements

- [ ] Resume upload → personalized questions
- [ ] Session history save (PDF export)
- [ ] Emotion detection from voice tone
- [ ] Multiple language support
- [ ] Webcam eye contact analysis
- [ ] Leaderboard / scoring history

---

## 👨‍💻 Author

**Hardik Jain**
B.Tech CSE (AI & DS) — AKS University, Satna

- GitHub: [@Hardik-8](https://github.com/Hardik-8/Hardik-8)
- Email: jainhardik819492@gmail.com

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
