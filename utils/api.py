# utils/api.py
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = "models/gemini-2.0-flash"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"

def call_gemini(
    user_text: str,
    system_preamble: str = "",
    history=None,
    temperature: float = 0.6,
    candidate=None,
    response_mime: str = "text/plain",
    phase: str = "",
):
    """
    Minimal wrapper for Gemini generateContent.
    - Sends 'system' style preface as the first user part.
    - Includes compact STATE (candidate + phase).
    - Optionally appends short history (last ~10 turns).
    Returns assistant text or raises RuntimeError.
    """
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is missing. Add it to your .env file.")

    contents = []

    # Emulated system + state preface
    preface_parts = []
    if system_preamble:
        preface_parts.append({"text": system_preamble})
    state_json = {"candidate": candidate or {}, "phase": phase or ""}
    preface_parts.append({"text": "STATE:\n" + json.dumps(state_json, indent=2)})
    preface_parts.append({"text": "\nAsk exactly one question at a time during data collection."})
    contents.append({"role": "user", "parts": preface_parts})

    # Short history
    if history:
        for turn in history[-10:]:
            role = turn.get("role", "user")
            text = turn.get("content", "")
            contents.append({"role": role, "parts": [{"text": text}]})

    # Latest user message
    contents.append({"role": "user", "parts": [{"text": user_text}]})

    payload = {
        "contents": contents,
        "generationConfig": {
            "temperature": temperature,
            "topK": 40,
            "topP": 0.9,
            "maxOutputTokens": 512,
            "responseMimeType": response_mime,
        },
        "safetySettings": []
    }

    resp = requests.post(GEMINI_URL, headers={"Content-Type": "application/json"}, json=payload, timeout=60)
    if resp.status_code != 200:
        raise RuntimeError(f"Gemini API error {resp.status_code}: {resp.text}")

    data = resp.json()
    try:
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception as e:
        raise RuntimeError(f"Unexpected Gemini response: {data}") from e
