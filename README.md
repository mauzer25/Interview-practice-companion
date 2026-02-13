# Interview Practice Companion

A Streamlit-based app that helps you prepare for job interviews using OpenAI's GPT models. Choose a practice mode, set your target role, and start practicing.

## Features

- **5 practice modes**, each using a different prompt engineering technique:
  - General Q&A (Zero-Shot)
  - Behavioral Interview with STAR method (Few-Shot)
  - Deep-Dive Questions (Chain-of-Thought)
  - Mock Interviewer (Role-Play)
  - Question Generator (Structured Output)
- **Customizable job role** — works for any position (Software Engineer, Data Analyst, Product Manager, etc.)
- **Temperature control** — adjust response creativity via sidebar slider
- **Multi-turn chat** — full conversation history within each session
- **Security guards** — input length limits, topic guardrails, API key validation

## Setup

1. **Clone the repo:**
   ```bash
   git clone https://github.com/mauzer25/Interview-practice-companion.git
   cd Interview-practice-companion
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Add your OpenAI API key:**
   ```bash
   cp .env.example .env
   # Edit .env and add your key
   ```

4. **Run the app:**
   ```bash
   streamlit run app.py
   ```

## Quick Start Guide

1. Launch the app with `streamlit run app.py` — it opens in your browser at `http://localhost:8501`
2. In the **sidebar**, pick a practice mode and enter the job role you're targeting
3. Type a message in the chat input at the bottom and hit Enter
4. The AI responds based on your selected mode — continue the conversation as long as you like
5. Use the **Clear Chat** button in the sidebar to start fresh

### Which mode should I use?

| Mode | Best for |
|------|----------|
| General Q&A | Quick answers to specific interview questions |
| Behavioral Interview | Practicing STAR-method answers for "Tell me about a time..." questions |
| Deep-Dive Questions | Working through complex problems step by step |
| Mock Interviewer | Simulating a real interview with back-and-forth Q&A and feedback |
| Question Generator | Getting a list of practice questions for a specific topic |

## Tech Stack

- [Streamlit](https://streamlit.io/) — frontend UI
- [OpenAI API](https://platform.openai.com/) — GPT-4o-mini for responses
- [python-dotenv](https://pypi.org/project/python-dotenv/) — environment variable management
