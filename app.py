import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

from prompts import PROMPTS

load_dotenv()

MAX_INPUT_LENGTH = 2000

MODE_ICONS = {
    "General Q&A (Zero-Shot)": "💡",
    "Behavioral Interview (Few-Shot)": "🗣️",
    "Deep-Dive Questions (Chain-of-Thought)": "🔍",
    "Mock Interviewer (Role-Play)": "🎭",
    "Question Generator (Structured Output)": "📋",
}

MODE_PLACEHOLDERS = {
    "General Q&A (Zero-Shot)": "Ask any interview question, e.g. 'What is polymorphism?'",
    "Behavioral Interview (Few-Shot)": "Enter a behavioral question or paste your draft STAR answer for feedback...",
    "Deep-Dive Questions (Chain-of-Thought)": "Ask a complex question, e.g. 'Design a URL shortener' or 'Explain event-driven architecture'",
    "Mock Interviewer (Role-Play)": "Say 'Hi' to start the mock interview, or describe the role you're targeting...",
    "Question Generator (Structured Output)": "Enter a topic, e.g. 'Python', 'System Design', 'Leadership'",
}

st.set_page_config(page_title="Interview Practice", page_icon="💼", layout="wide")

# --- Custom CSS ---
st.markdown("""
<style>
    .mode-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 0.85em;
        font-weight: 500;
        background: #e8f0fe;
        color: #1a73e8;
        margin-bottom: 8px;
    }
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 16px 20px;
        border-radius: 12px;
        color: white;
        text-align: center;
    }
    .stat-card h3 {
        margin: 0;
        font-size: 1.8em;
    }
    .stat-card p {
        margin: 4px 0 0 0;
        opacity: 0.85;
        font-size: 0.9em;
    }
    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9fc 0%, #eef1f6 100%);
    }
    .welcome-box {
        border: 1px solid rgba(128, 128, 128, 0.2);
        padding: 24px;
        border-radius: 12px;
        margin-bottom: 16px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.markdown("## ⚙️ Settings")

mode = st.sidebar.selectbox(
    "Practice Mode",
    options=list(PROMPTS.keys()),
    format_func=lambda m: f"{MODE_ICONS.get(m, '')} {m}",
    help="Each mode uses a different prompting technique.",
)

job_role = st.sidebar.text_input(
    "🎯 Job Role",
    value="Software Engineer",
    help="The role you're preparing to interview for.",
)

with st.sidebar.expander("ℹ️ About this mode", expanded=False):
    st.markdown(PROMPTS[mode]["description"])

st.sidebar.markdown("---")
st.sidebar.markdown("#### Fine-tuning")

temperature = st.sidebar.slider(
    "🌡️ Temperature",
    min_value=0.0,
    max_value=1.5,
    value=0.7,
    step=0.1,
    help=(
        "Controls randomness. Lower values (0.0-0.3) give focused, deterministic "
        "answers. Higher values (0.8-1.5) give more creative, varied responses."
    ),
)

st.sidebar.markdown("---")

if st.sidebar.button("🗑️ Clear Chat", use_container_width=True):
    st.session_state.messages = []
    st.rerun()

# --- API Key Validation ---
api_key = os.getenv("OPENAI_API_KEY")
if not api_key or api_key == "your-key-here":
    st.error(
        "OpenAI API key not found. Please create a `.env` file with your key:\n\n"
        "```\nOPENAI_API_KEY=sk-...\n```"
    )
    st.stop()

client = OpenAI(api_key=api_key)

# --- Header ---
col1, col2, col3 = st.columns([2, 5, 2])
with col2:
    st.markdown(f"# {MODE_ICONS.get(mode, '💼')} Interview Practice")
    st.caption(f"Preparing for: **{job_role}** | Mode: **{mode}**")

# --- Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_mode" not in st.session_state:
    st.session_state.current_mode = mode
if "current_role" not in st.session_state:
    st.session_state.current_role = job_role

# Reset chat when mode or role changes
if st.session_state.current_mode != mode or st.session_state.current_role != job_role:
    st.session_state.messages = []
    st.session_state.current_mode = mode
    st.session_state.current_role = job_role

# Show welcome message when chat is empty
if not st.session_state.messages:
    st.markdown(f"""
<div class="welcome-box">
    <h3>{MODE_ICONS.get(mode, '💼')} Ready to practice!</h3>
    <p>You're in <strong>{mode}</strong> mode, preparing for a <strong>{job_role}</strong> role.</p>
    <p style="opacity: 0.7; margin-top: 8px;">Type a message below to get started.</p>
</div>
""", unsafe_allow_html=True)

    # Quick-start suggestions
    st.markdown("**Quick start suggestions:**")
    suggestions = {
        "General Q&A (Zero-Shot)": [
            "What are the SOLID principles?",
            "Explain the difference between REST and GraphQL",
            "How does garbage collection work?",
        ],
        "Behavioral Interview (Few-Shot)": [
            "Tell me about a time you dealt with a tight deadline",
            "Describe a situation where you had to learn something new quickly",
            "Give an example of when you disagreed with your manager",
        ],
        "Deep-Dive Questions (Chain-of-Thought)": [
            "Design a URL shortening service",
            "How would you build a real-time chat application?",
            "Explain how a database index works internally",
        ],
        "Mock Interviewer (Role-Play)": [
            "Hi, I'm ready for my interview!",
            "I'd like to practice for a senior role",
            "Let's start with technical questions",
        ],
        "Question Generator (Structured Output)": [
            "Python and data structures",
            "System design and scalability",
            "Leadership and team management",
        ],
    }
    cols = st.columns(3)
    for i, suggestion in enumerate(suggestions.get(mode, [])):
        with cols[i]:
            st.code(suggestion, language=None)

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Stats in sidebar
if st.session_state.messages:
    user_msgs = sum(1 for m in st.session_state.messages if m["role"] == "user")
    st.sidebar.markdown("---")
    st.sidebar.markdown("#### 📊 Session Stats")
    st.sidebar.metric("Questions Asked", user_msgs)
    st.sidebar.metric("Total Messages", len(st.session_state.messages))

# --- User Input ---
placeholder = MODE_PLACEHOLDERS.get(mode, "Type your question or answer here...")
user_input = st.chat_input(placeholder)

if user_input:
    # Security: input length limit
    if len(user_input) > MAX_INPUT_LENGTH:
        st.error(
            f"Input too long ({len(user_input)} characters). "
            f"Please keep it under {MAX_INPUT_LENGTH} characters."
        )
        st.stop()

    # Add user message to history and display
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Build messages for API call
    system_prompt = PROMPTS[mode]["system"].format(role=job_role)
    api_messages = [{"role": "system", "content": system_prompt}]
    for msg in st.session_state.messages:
        api_messages.append({"role": msg["role"], "content": msg["content"]})

    # Call OpenAI API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=api_messages,
                    temperature=temperature,
                )
                assistant_message = response.choices[0].message.content
                st.markdown(assistant_message)
                st.session_state.messages.append(
                    {"role": "assistant", "content": assistant_message}
                )
            except Exception as e:
                st.error(f"Error calling OpenAI API: {e}")
