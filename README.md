# ai-hiring-bot

Talent Scout is an AI-powered multilingual hiring assistant chatbot designed to streamline the candidate screening process. It interacts conversationally with candidates, collects their information, asks dynamic technical questions based on their tech stack, provides feedback, and records their profiles — making the initial hiring stage more efficient and scalable.

Built with Python, Streamlit, and LLM (Large Language Models)

## Installation Instructions
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/smart-hire-chatbot.git
   cd smart-hire-chatbot

2. **Create and Activate Virtual Environment (Optional but recommended)**:

    ```bash
    python -m venv venv
    source venv/bin/activate  # For Linux/Mac
    venv\Scripts\activate     # For Windows

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt

4. **Run the Application**:

    ```bash
    streamlit run main.py

# Access: Open the displayed local URL in your browser (e.g., http://localhost:8501).

# Usage Guide
Launch the app.

Home page welcomes the candidate with "Smart Hire" branding.

Candidate selects preferred language.

Bot greets the candidate in their chosen language and collects personal and professional details.

Based on the tech stack, the chatbot generates 3–4 dynamic technical questions.

Candidates answer, get feedback after each question, and are asked if they want to continue or exit.

Upon completion or exit, profiles are recorded, and final feedback is given (if interview is completed).

Application returns to home for the next candidate.


# Technical Details
Language: Python 3.10+

Framework: Streamlit

LLM Model: gpt-3.5 OPEN_AI

Other Libraries:

langchain

streamlit

re (for regex validation)

dotenv (for environment variable management)

# Architecture:

main.py - Streamlit app runner and UI logic

model.py - LLM model interface and query handling

prompts.py - Prompt templates for different conversation stages

Modular design for easy updates and maintainability.

# Prompt Design
Greeting Prompt: Welcomes the candidate in their selected language.

Information Gathering Prompt: Politely and systematically collects candidate details.

Question Generation Prompt: Based on tech stack and experience, dynamically generates custom technical questions.

Feedback Prompt: Summarizes performance based on answer accuracy and provides encouragement or improvement areas.