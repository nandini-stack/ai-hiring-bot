import streamlit as st
from prompts import get_greeting_prompt, get_question_prompt, get_feedback_prompt, get_final_feedback_prompt
from model import get_llm_response, evaluate_answer
import re
import time

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_phone(phone):
    return re.match(r"^\d{10}$", phone)


def load_css():
    return """
    <style>
        body {
            background-color: #f4f6f9;
            font-family: 'Segoe UI', sans-serif;
            color: #333333;
        }
        .custom-header {
            text-align: center;
            background-color: #004080;
            padding: 20px;
            color: white;
            border-radius: 12px;
            margin-bottom: 20px;
        }
        /* Override Streamlit form styling */
        .stForm {
            background-color: #ffffff;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            margin: 0 auto 25px auto;
            width: 80%;
        }
        .stForm input[type="text"],
        .stForm input[type="email"] {
            padding: 12px;
            # margin: 10px 0;
            width: 100%;
            border: 1px solid #ccc;
            border-radius: 8px;
            font-size: 16px;
        }
        .stForm button {
            background-color: #004080;
            color: white;
            padding: 10px 20px;
            border-radius: 8px;
            font-weight: bold;
            border: none;
            cursor: pointer;
        }
        .stForm button:hover {
            background-color: #003060;
        }
      .custom-question {
            background-color: #f0f4ff;
            padding: 20px;
            margin-top: 20px;
            border-radius: 12px;
            font-size: 18px;
            font-weight: 500;
            color: #003060;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        }
        .custom-footer {
            text-align: center;
            margin-top: 40px;
            font-size: 18px;
            color: #004080;
        }
    </style>
    """

def display_home_page():
    st.markdown('<div class="custom-header"><h1>Welcome to Talent Scout</h1><p>Your first step towards getting hired!</p></div>', unsafe_allow_html=True)
    st.markdown('<p>Let\'s start with your interview. Click the button below to begin.</p>', unsafe_allow_html=True)

    lang = st.selectbox("Choose your language / अपनी भाषा चुनें:", ["English", "Hindi", "Spanish"])
    if st.button("Start Interview"):
        st.session_state.candidate["language"] = lang
        st.session_state.stage = "greeting"
        st.rerun()


st.markdown(load_css(), unsafe_allow_html=True)


if "stage" not in st.session_state:
    st.session_state.stage = "home"
    st.session_state.candidate = {}
    st.session_state.questions = []
    st.session_state.answers = []
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.feedback = ""
    st.session_state.waiting_confirmation = False

if st.session_state.stage == "home":
    display_home_page()

elif st.session_state.stage == "greeting":
    st.write(get_llm_response(get_greeting_prompt(st.session_state.candidate["language"])))
    with st.form("candidate_details"):
        st.session_state.candidate["name"] = st.text_input("Full Name")
        st.session_state.candidate["email"] = st.text_input("Email Address")
        st.session_state.candidate["phone"] = st.text_input("Phone Number")
        st.session_state.candidate["experience"] = st.text_input("Years of Experience")
        st.session_state.candidate["position"] = st.text_input("Desired Position(s)")
        st.session_state.candidate["location"] = st.text_input("Current Location")
        st.session_state.candidate["tech_stack"] = st.text_input("Tech Stack (comma-separated)")
        st.markdown('</div>', unsafe_allow_html=True)
    
        if st.form_submit_button("Submit"):
            candidate = st.session_state.candidate
            if not all([
                candidate["name"],
                candidate["email"],
                candidate["phone"],
                candidate["experience"],
                candidate["position"],
                candidate["location"],
                candidate["tech_stack"]
            ]):
                st.error("Please fill in all the required fields.")
            elif not is_valid_email(candidate["email"]):
                st.error("Please enter a valid email address.")
            elif not is_valid_phone(candidate["phone"]):
                st.error("Please enter a valid 10-digit phone number.")
            else:
                st.session_state.stage = "generate_questions"
                st.rerun()


elif st.session_state.stage == "generate_questions":
    prompt = get_question_prompt(
        st.session_state.candidate["tech_stack"],
        st.session_state.candidate["experience"],
        st.session_state.candidate["language"],
    )
    response = get_llm_response(prompt)
    st.session_state.questions = [q.strip() for q in response.split("\n") if q.strip()]
    st.session_state.stage = "interview"
    st.rerun()

elif st.session_state.stage == "interview":
    if st.session_state.current_q >= len(st.session_state.questions):
            st.session_state.stage = 'final'
            st.session_state.waiting_confirmation = False
            st.rerun()

    q = st.session_state.questions[st.session_state.current_q]
    st.markdown(f'<div class="custom-question"><strong>Q{st.session_state.current_q + 1}:</strong> {q}</div>', unsafe_allow_html=True)

    if len(st.session_state.answers) <= st.session_state.current_q:
        answer = st.text_input("Your Answer:", key=f"ans_{st.session_state.current_q}")
        if st.button("Submit Answer"):
            is_correct = evaluate_answer(q, answer)
            feedback = "Correct answer." if is_correct else "Incorrect answer."
            st.session_state.answers.append({
                "question": q,
                "answer": answer,
                "feedback": feedback,
                "is_correct": is_correct
            })
            st.session_state.feedback = feedback
            st.session_state.waiting_confirmation = True

            if is_correct:
                st.session_state.score += 1

            st.rerun()
    else:
        st.session_state.feedback = st.session_state.answers[st.session_state.current_q]["feedback"]
        st.session_state.waiting_confirmation = True

if st.session_state.waiting_confirmation and st.session_state.current_q < len(st.session_state.questions):
        st.write(st.session_state.feedback)
        cont = st.text_input("Say 'yes' to continue, 'no' to exit:", key=f"cont_{st.session_state.current_q}")
        if cont.lower() in ["yes", "y", "ok"]:
            st.session_state.current_q += 1
            st.session_state.waiting_confirmation = False
            st.session_state.feedback = ""
            if st.session_state.current_q >= len(st.session_state.questions):
                st.session_state.stage = "final"
            st.rerun()
        elif cont.lower() in ["no", "n"]:
                st.write("Thank you. Your profile has been recorded.")
                st.session_state.stage = "home" 
                time.sleep(1)
                st.session_state.clear()
                st.rerun()
           

elif st.session_state.stage == "final":
    final_prompt = get_final_feedback_prompt(
        st.session_state.score,
        len(st.session_state.questions),
        st.session_state.candidate["language"]
    )
    st.markdown('<div class="custom-footer">', unsafe_allow_html=True)
    st.write(get_llm_response(final_prompt))
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()
