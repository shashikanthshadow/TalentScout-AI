# utils/context.py
import re
from typing import Dict, Any, List
from .api import call_gemini
from prompts import SYSTEM_PROMPT

# Permissive demo validators
RE_EMAIL = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
RE_PHONE = re.compile(r"^[+]?\d[\d\s().-]{6,}$")

def first_missing_field(candidate: Dict[str, Any], collection_order: List = None) -> str:
    """
    Return the first field key that is None/empty, or "" if all present.
    """
    from prompts import COLLECTION_ORDER
    order = collection_order or COLLECTION_ORDER
    for key, _ in order:
        val = candidate.get(key)
        if val is None or (isinstance(val, str) and not val.strip()):
            return key
    return ""

def validate_and_store(field: str, user_text: str, candidate: Dict[str, Any], set_error) -> bool:
    """
    Validate and store user's response into candidate dict.
    set_error: callback to set UI error message (e.g., st.session_state.error)
    Returns True on success, False on validation failure.
    """
    val = (user_text or "").strip()
    if field == "email":
        if not RE_EMAIL.match(val):
            set_error("That doesn't look like a valid email. Please try again.")
            return False
    elif field == "phone":
        if not RE_PHONE.match(val):
            set_error("That phone number seems invalid. Use digits with optional +, spaces, or dashes.")
            return False
    elif field == "years_experience":
        try:
            years = float(val)
            if years < 0 or years > 60:
                set_error("Please enter years of experience between 0 and 60.")
                return False
            val = years
        except ValueError:
            set_error("Please enter a numeric value for years of experience.")
            return False

    candidate[field] = val
    set_error(None)
    return True

def generate_questions_with_gemini(tech_stack_text: str, candidate: Dict[str, Any], history):
    """
    Ask Gemini to generate grouped questions (3–5 per technology) for the provided stack.
    """
    prompt = (
        "Generate tailored technical interview questions based on the candidate's tech stack.\n"
        f"Tech stack provided: {tech_stack_text}\n"
        "For each distinct technology mentioned, provide 3-5 questions mixing basic, intermediate, and advanced.\n"
        "Group by technology with a short heading. Keep questions concise and job-relevant.\n"
    )
    return call_gemini(
        user_text=prompt,
        system_preamble=SYSTEM_PROMPT,
        history=history,
        candidate=candidate,
        phase="questions",
    )
