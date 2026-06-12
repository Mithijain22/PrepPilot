import streamlit as st
import os
from core.stt import record_audio, transcribe_audio
from core.tts import speak
from core.interview_engine import InterviewEngine

# ── Page Config ──────────────────────────────────────
st.set_page_config(
    page_title="AI Voice Interviewer",
    page_icon="🎙️",
    layout="centered"
)

# ── Custom CSS ───────────────────────────────────────
st.markdown("""
    <style>
        .main { background-color: #0e1117; }
        .stButton>button {
            background-color: #1f77b4;
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 16px;
            border: none;
        }
        .stButton>button:hover {
            background-color: #155a8a;
        }
        .feedback-box {
            background-color: #1a2a1a;
            border-left: 4px solid #00ff88;
            padding: 15px;
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────
st.markdown("# 🎙️ AI Voice Interviewer")
st.markdown("*Practice interviews with AI — speak or type your answers*")
st.divider()

# ── Session State Init ───────────────────────────────
if "engine" not in st.session_state:
    st.session_state.engine = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "interview_active" not in st.session_state:
    st.session_state.interview_active = False
if "feedback" not in st.session_state:
    st.session_state.feedback = None

# ── Sidebar ──────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Interview Settings")

    company = st.selectbox(
        "🏢 Company",
        ["Google", "Amazon", "Microsoft", "Meta", "Apple",
        "Netflix", "Twitter/X", "LinkedIn", "Uber", "Airbnb",
        
        # 🇺🇸 Other US Tech
        "Salesforce", "Adobe", "Oracle", "IBM", "Intel",
        "Nvidia", "Qualcomm", "Cisco", "VMware", "Stripe",
        "Dropbox", "Atlassian", "Palantir", "Snowflake", "DataBricks",
        "OpenAI", "Anthropic", "DeepMind", "Spotify", "PayPal",
        
        # 🇮🇳 Indian IT / Product
        "Infosys", "TCS", "Wipro", "HCL", "Tech Mahindra",
        "Flipkart", "Zomato", "Swiggy", "Ola", "Paytm",
        "CRED", "Razorpay", "Freshworks", "Zoho", "PhonePe",
        "Meesho", "Zerodha", "Groww", "Dream11", "Byju's",
        
        # 🌏 Global
        "Samsung", "Sony", "Accenture", "Capgemini", "Cognizant"],
        disabled=st.session_state.interview_active
    )

    role = st.selectbox(
        "💼 Role",
        ["SDE", "Data Scientist", "ML Engineer", "Backend Developer", "Frontend Developer", "DevOps Engineer"],
        disabled=st.session_state.interview_active
    )

    difficulty = st.selectbox(
        "📊 Difficulty",
        ["easy", "medium", "hard"],
        format_func=lambda x: x.capitalize(),
        disabled=st.session_state.interview_active
    )

    recording_duration = st.slider(
        "🎤 Recording Duration (seconds)",
        min_value=5,
        max_value=30,
        value=10
    )

    st.divider()

    # Stats
    if st.session_state.engine:
        st.subheader("📈 Session Stats")
        total = st.session_state.engine.total_questions()
        st.metric("Questions Answered", total)

    st.divider()

    start_btn = st.button(
        "🚀 Start Interview",
        disabled=st.session_state.interview_active,
        use_container_width=True
    )

    reset_btn = st.button(
        "🔄 Reset",
        use_container_width=True
    )

# ── Reset Logic ───────────────────────────────────────
if reset_btn:
    st.session_state.engine = None
    st.session_state.chat_history = []
    st.session_state.interview_active = False
    st.session_state.feedback = None
    st.rerun()

# ── Start Interview Logic ────────────────────────────
if start_btn:
    engine = InterviewEngine(company, role, difficulty)
    st.session_state.engine = engine
    st.session_state.interview_active = True
    st.session_state.chat_history = []
    st.session_state.feedback = None

    with st.spinner("🤖 Generating your first question..."):
        question = engine.load_starter_question()

    st.session_state.chat_history.append(("Interviewer", question))

    try:
        speak(question)
    except Exception as e:
        st.warning(f"TTS Error (continuing without audio): {e}")

    st.rerun()

# ── Chat History Display ─────────────────────────────
if st.session_state.chat_history:
    st.subheader("💬 Interview Conversation")

    for speaker, msg in st.session_state.chat_history:
        if speaker == "Interviewer":
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(f"**Interviewer:** {msg}")
        else:
            with st.chat_message("user", avatar="👤"):
                st.markdown(f"**You:** {msg}")

# ── Voice & Text Input ───────────────────────────────
if st.session_state.interview_active:
    st.divider()
    st.subheader("🎤 Your Answer")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Option 1 — Voice**")
        if st.button(f"🎤 Record ({recording_duration}s)", use_container_width=True):
            with st.spinner(f"🔴 Recording for {recording_duration} seconds..."):
                try:
                    audio_path = record_audio(duration=recording_duration)
                except Exception as e:
                    st.error(f"Recording error: {e}")
                    audio_path = None

            if audio_path:
                with st.spinner("📝 Transcribing... please wait"):
                    try:
                        answer = transcribe_audio(audio_path)
                        st.success(f"✅ Transcribed: *{answer}*")
                    except Exception as e:
                        st.error(f"Transcription error: {e}")
                        answer = None

                if answer:
                    st.session_state.chat_history.append(("You", answer))

                    with st.spinner("🤔 Generating follow-up question..."):
                        followup = st.session_state.engine.get_followup(answer)

                    st.session_state.chat_history.append(("Interviewer", followup))

                    try:
                        speak(followup)
                    except Exception as e:
                        st.warning(f"TTS skipped: {e}")

                    st.rerun()

    with col2:
        st.markdown("**Option 2 — Type**")
        typed_answer = st.text_area(
            "Type your answer here:",
            height=120,
            key="typed_input",
            label_visibility="collapsed",
            placeholder="Type your answer here..."
        )

        if st.button("✅ Submit Answer", use_container_width=True):
            if typed_answer.strip():
                answer = typed_answer.strip()
                st.session_state.chat_history.append(("You", answer))

                with st.spinner("🤔 Generating follow-up question..."):
                    followup = st.session_state.engine.get_followup(answer)

                st.session_state.chat_history.append(("Interviewer", followup))

                try:
                    speak(followup)
                except Exception as e:
                    st.warning(f"TTS skipped: {e}")

                st.rerun()
            else:
                st.warning("Please type something before submitting!")

    st.divider()

    # End Interview Button
    col_end1, col_end2, col_end3 = st.columns([1, 2, 1])
    with col_end2:
        if st.button("🏁 End Interview & Get Feedback", use_container_width=True):
            if st.session_state.engine.total_questions() == 0:
                st.warning("Answer at least one question before ending!")
            else:
                with st.spinner("📊 Analyzing your performance..."):
                    feedback = st.session_state.engine.get_feedback()

                st.session_state.feedback = feedback
                st.session_state.interview_active = False
                st.rerun()

# ── Feedback Display ─────────────────────────────────
if st.session_state.feedback:
    st.divider()
    st.subheader("📊 Performance Feedback")

    st.markdown(
        f"""
        <div class="feedback-box">
            {st.session_state.feedback.replace(chr(10), '<br>')}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()
    col_r1, col_r2, col_r3 = st.columns([1, 2, 1])
    with col_r2:
        if st.button("🔄 Start New Interview", use_container_width=True):
            st.session_state.engine = None
            st.session_state.chat_history = []
            st.session_state.interview_active = False
            st.session_state.feedback = None
            st.rerun()

# ── Empty State ──────────────────────────────────────
if not st.session_state.chat_history and not st.session_state.interview_active:
    st.markdown("""
        <div style='text-align: center; padding: 50px; color: #888;'>
            <h3>👈 Configure settings and click Start Interview</h3>
            <p>Choose your company, role, and difficulty from the sidebar</p>
            <p>🎙️ Voice + ⌨️ Text input both supported</p>
        </div>
    """, unsafe_allow_html=True)