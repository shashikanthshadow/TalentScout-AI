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

