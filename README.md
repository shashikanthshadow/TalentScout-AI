# 🧭 TalentScout Hiring Assistant

An AI-powered hiring assistant chatbot built with **Streamlit** and **Google Gemini 2.0 Flash**, designed to help recruiters collect candidate information and generate tailored technical questions based on the candidate’s declared tech stack.  

---

## 🚀 Features

- 🤝 **Greeting & Introduction** – Welcomes candidates, explains purpose, and informs them they can exit anytime.  
- 📝 **Information Gathering** – Collects:
  - Full Name  
  - Email Address  
  - Phone Number  
  - Years of Experience  
  - Desired Position(s)  
  - Current Location  
  - Tech Stack  
- ⚡ **Dynamic Tech Questions** – Generates 3–5 technical questions based on the declared tech stack.  
- 🔄 **Context-Aware Flow** – Maintains conversation context for smooth interactions.  
- 🛡️ **Privacy by Design** – Candidate data is only stored in the session (no server persistence in this demo).  
- 📥 **Export Snapshot** – Download candidate details as CSV (local demo).  
- 🖥️ **Reset Conversation** – Start over anytime with a single click.  

---

## 🛠️ Tech Stack

- **Language**: Python 3.9+  
- **Frontend**: [Streamlit](https://streamlit.io/)  
- **LLM API**: [Google Gemini 2.0 Flash](https://ai.google.dev/)  
- **Environment**: Conda virtual environment  
- **Other Tools**:  
  - `python-dotenv` – for API key management  
  - `pandas` – for candidate export  
  - `requests` – for API calls  

---

## 📂 Project Structure
``` bash
TalentScout AI│
├── app.py # Main Streamlit app
├── prompts.py # Prompt templates & collection order
├── utils/
│ ├── api.py # Gemini API call helper
│ ├── context.py # Context management & validation
│ ├── storage.py # Candidate export utilities
│
├── requirements.txt # Python dependencies
├── .env.example # Example env file (no secrets)
└── README.md # Project documentation

```
---

## ⚙️ Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/talentscout-hiring-assistant.git
cd talentscout-hiring-assistant
```

### 2. Create and Activate Conda Environment
```bash
conda create -n talentscout python=3.10 -y
conda activate talentscout
```
### 3. Install Dependencies
``` bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a .env file in the project root:
```
GEMINI_API_KEY=your_google_gemini_api_key_here
```
(Get your API key from Google AI Studio
)
---

## ▶️ Run the Project
streamlit run app.py


App will open in your browser at: http://localhost:8501
---
## 🎥 Demo

Option 1: Record a short Loom
 walkthrough showing interaction.

Option 2: Deploy on Streamlit Cloud
 and share the live URL.
---
## 🔒 Data & Privacy

This demo does not persist data.

All candidate information is stored only in st.session_state and cleared upon reset or browser refresh.

For production:

Use encrypted databases, access control, and comply with GDPR/DPDP standards.

## ✨ Optional Enhancements

### 🌍 Multilingual support
- **Goal:** Let candidates chat in their preferred language; detect & respond accordingly.
- **How:**
  - Add a language selector (or auto-detect first message and set a `lang` in session).
  - Pass `lang` into the system prompt and ask the model to reply in that language.
  - Optionally translate UI labels via a small dict: `{"en": {...}, "hi": {...}}`.
- **Code sketch:**
  ```python
  # In Streamlit sidebar
  lang = st.sidebar.selectbox("Language", ["en", "hi", "fr", "es"])
  st.session_state.lang = lang

  # In SYSTEM_PROMPT or API call
  system_preamble = SYSTEM_PROMPT + f"\nRespond in language code: {lang}."
```
