def get_greeting_prompt(language):
    return f"""
    Generate a short and polite greeting message in {language}. Don't mention any name or company. simple plain text is required. Mention that you are a hiring assistant and will ask for basic details and technical questions.
    """

def get_question_prompt(tech_stack,experience,language):
    return f"""
    You are a hiring assistant. Based on the following tech stack: {tech_stack}, and considering the candidate having {experience} years in the domain generate 3 to 4 technical interview questions.Do NOT number the questions.Respond only with plain text questions.
    The questions should be concise and in {language}. Only return the questions separated by new lines.
    """

def get_feedback_prompt(question, answer, language):
    return f"""
    Evaluate the candidate's answer to this question:

    Question: {question}
    Answer: {answer}

    In {language}, provide feedback. If the answer is correct, appreciate and say we’ll move to the next question. If it's incorrect, say it's incorrect and we’ll move on.
    """

def get_final_feedback_prompt(score, total, language):
    percentage = (score / total) * 100
    if percentage >= 70:
        return f"""
        In {language}, thank the candidate for completing the interview. Congratulate them for scoring {percentage:.0f}% and inform them they’ll proceed to the next round.
        """
    else:
        return f"""
        In {language}, thank the candidate for participating. Inform them they scored {percentage:.0f}% and unfortunately didn’t qualify this time. Wish them luck.
        """
