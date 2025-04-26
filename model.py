from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
import os
import streamlit as st
from dotenv import load_dotenv



load_dotenv()
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

llm = ChatOpenAI(
    temperature=0.3,
    model_name="gpt-3.5-turbo",
    openai_api_key=OPENAI_API_KEY
)

def get_llm_response(prompt: str) -> str:
    messages = [HumanMessage(content=prompt)]
    response = llm.invoke(messages)
    return response.content

def evaluate_answer(question, answer):
    eval_prompt = f"""
    Evaluate the following candidate's answer to an interview question:

    Question: {question}
    Answer: {answer}

    Please evaluate the quality of the answer:
    - Reply with 'proceed%next%' if the answer is mostly correct, demonstrating solid knowledge and practical suggestions.
    - Reply with 'incorrect%ans%' if the answer lacks key components or is technically inaccurate.

    Please provide detailed feedback if possible.
    """

  
    result = get_llm_response(eval_prompt).strip()
    result = result.replace("\n", " ")  

    if "proceed%next%" in result.lower():     
        return True
      
    elif "incorrect%ans%" in result.lower():
        return False
   