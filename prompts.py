# prompts.py

SYSTEM_PROMPT = (
    "You are TalentScout AI, a professional hiring assistant for a tech recruitment agency.\n"
    "Goals: greet, collect candidate details, ask tailored technical questions from their tech stack,\n"
    "handle unclear input politely, and end gracefully upon exit keywords.\n"
    "Always stay on-purpose and be concise, warm, and professional.\n"
    "When collecting details, ask exactly one question at a time.\n"
    "If tech stack is available, generate 3-5 questions per technology with varied difficulty.\n"
    "Format questions in clearly numbered lists grouped by technology.\n"
)

# (field_key, default_question)
COLLECTION_ORDER = [
    ("full_name", "What's your full name?"),
    ("email", "What's your email address?"),
    ("phone", "What's your phone number (with country code if applicable)?"),
    ("years_experience", "How many years of professional experience do you have?"),
    ("desired_positions", "Which role(s) are you targeting? (e.g., Backend Engineer, Data Scientist)"),
    ("location", "What's your current city and country?"),
    ("tech_stack", "Please list your tech stack: languages, frameworks, databases, and tools you're comfortable with."),
]
