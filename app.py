"""
TalentScout Hiring Assistant — Streamlit + Gemini 2.0 Flash (Modular)
Run:
1) conda activate talentscout
2) pip install -r requirements.txt
3) Create .env with GEMINI_API_KEY=your_key
4) streamlit run app.py
"""

import streamlit as st
from dotenv import load_dotenv

from utils.api import call_gemini
from utils.context import first_missing_field, validate_and_store, generate_questions_with_gemini
from utils.storage import candidate_to_dataframe, merge_tech_stack
from prompts import SYSTEM_PROMPT, COLLECTION_ORDER

# -----------------------------
# Environment
# -----------------------------
load_dotenv()

# -----------------------------
# Streamlit Page Config
# -----------------------------
st.set_page_config(
    page_title="TalentScout Hiring Assistant",
    page_icon="🧭",
    layout="centered",
)

st.title("🧭 TalentScout — Hiring Assistant (Gemini)")
st.caption("Collects candidate info and generates tailored technical questions based on the declared tech stack.")

with st.expander("Data & Privacy", expanded=False):
    st.write(
        """
        **Demo Disclaimer**: This demo does **not** persist data on a server. 
        Your inputs live only in this browser session (`st.session_state`). For a real deployment, 
        integrate secure storage (encrypted at rest, access controls) and follow GDPR/DPDP guidelines.
        """
    )

# -----------------------------
# Session State Initialization
# -----------------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "candidate" not in st.session_state:
    st.session_state.candidate = {field: None for field, _ in COLLECTION_ORDER}

if "phase" not in st.session_state:
    st.session_state.phase = "intro"  # intro → collecting → questions → ended

if "questions" not in st.session_state:
    st.session_state.questions = []

if "error" not in st.session_state:
    st.session_state.error = None

def set_error(msg):
    st.session_state.error = msg

EXIT_KEYWORDS = {"exit", "quit", "end", "stop", "bye", "goodbye"}

# -----------------------------
# Chat Rendering Helpers
# -----------------------------
def ai_say(text: str):
    st.session_state.history.append({"role": "assistant", "content": text})
    with st.chat_message("assistant"):
        st.markdown(text)

def user_say(text: str):
    st.session_state.history.append({"role": "user", "content": text})
    with st.chat_message("user"):
        st.markdown(text)

# -----------------------------
# Intro Greeting (once)
# -----------------------------
if st.session_state.phase == "intro":
    greeting = call_gemini(
        user_text=(
            "Greet the candidate. Briefly explain you're here to collect some basics and then ask tailored tech questions.\n"
            "Politely mention they can type 'exit' anytime to finish. Ask the first question from the collection order."
        ),
        system_preamble=SYSTEM_PROMPT,
        candidate=st.session_state.candidate,
        phase="intro",
    )
    ai_say(greeting)
    st.session_state.phase = "collecting"

# -----------------------------
# Display prior history
# -----------------------------
for turn in st.session_state.history:
    with st.chat_message(turn["role"]):
        st.markdown(turn["content"])

# -----------------------------
# Chat Input
# -----------------------------
prompt = st.chat_input("Type your message… (or 'exit' to finish)")

if prompt:
    # Exit handling
    if any(word in prompt.lower() for word in EXIT_KEYWORDS):
        user_say(prompt)
        ai_say("Thanks for your time! We'll review your details and reach out with next steps. Have a great day!")
        st.session_state.phase = "ended"
        st.stop()

    user_say(prompt)

    # COLLECTION / QUESTIONS FLOW
    if st.session_state.phase in {"collecting", "questions"}:
        missing = first_missing_field(st.session_state.candidate)
        if missing:
            # We still need to collect something
            if validate_and_store(missing, prompt, st.session_state.candidate, set_error):
                # Ask for next missing field
                next_missing = first_missing_field(st.session_state.candidate)
                if next_missing:
                    hint = dict(COLLECTION_ORDER)[next_missing]
                    follow_up = call_gemini(
                        user_text=(f"Ask the candidate for '{next_missing}'. Use this hint: '{hint}'. "
                                   "Ask one concise question only."),
                        system_preamble=SYSTEM_PROMPT,
                        history=st.session_state.history,
                        candidate=st.session_state.candidate,
                        phase="collecting",
                    )
                    ai_say(follow_up)
                else:
                    # Finished collection; move to questions phase
                    st.session_state.phase = "questions"
                    tech = (st.session_state.candidate.get("tech_stack") or "").strip()
                    if not tech:
                        ai_say("I didn't catch your tech stack. Could you list your languages, frameworks, databases, and tools?")
                    else:
                        with st.spinner("Generating tailored technical questions…"):
                            try:
                                qtext = generate_questions_with_gemini(tech, st.session_state.candidate, st.session_state.history)
                                st.session_state.questions = [{"tech": "(see below)", "questions": []}]
                                ai_say(qtext)
                                ai_say("If you'd like to add or change your tech stack, type it in. Otherwise, type 'exit' to conclude.")
                            except Exception:
                                ai_say("Sorry, I ran into an issue generating questions. Please try again.")
            else:
                ai_say(st.session_state.error)
        else:
            # Already have all details; treat input as tech stack update or follow-up
            if st.session_state.phase != "questions":
                st.session_state.phase = "questions"
            with st.spinner("Refreshing questions…"):
                try:
                    prev = st.session_state.candidate.get("tech_stack")
                    merged = merge_tech_stack(prev, prompt)
                    st.session_state.candidate["tech_stack"] = merged
                    qtext = generate_questions_with_gemini(merged, st.session_state.candidate, st.session_state.history)
                    ai_say(qtext)
                    ai_say("You can continue refining your stack or type 'exit' to finish.")
                except Exception:
                    ai_say("Couldn't generate questions right now. Please try again.")

# -----------------------------
# Sidebar: Live Candidate Snapshot
# -----------------------------
with st.sidebar:
    st.subheader("📇 Candidate Snapshot")
    st.json(st.session_state.candidate)

    st.subheader("📄 Export (local, demo)")
    df = candidate_to_dataframe(st.session_state.candidate)
    st.download_button(
        "Download CSV (demo)",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="candidate_demo.csv",
        mime="text/csv",
        use_container_width=True,
    )

    st.subheader("⚙️ Controls")
    if st.button("Reset Conversation", use_container_width=True):
        for key in ["history", "candidate", "phase", "questions", "error"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()  # ✅ replaced deprecated experimental_rerun

    st.caption("Powered by Google Gemini 2.0 Flash • Streamlit")
