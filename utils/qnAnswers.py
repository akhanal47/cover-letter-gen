import os
import tempfile
from pathlib import Path
import streamlit as st
import PyPDF2
from docx import Document
from openai import OpenAI
from fpdf import FPDF
import re
import random
import json

def load_qa_prompts():
    current_dir = os.path.dirname(__file__)
    filepath = os.path.join(current_dir, "prompt.json")
    
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
    except Exception:
        return None

def question_sys_prompt(qa_writing_style):
    prompts = load_qa_prompts()
    
    default_sys = f"You are an expert Software Developer, given the Candidate resume; job description and provided question write a response to that question. Answer as if your are the candidate and you are answering the question. Make the answer short. Do not include any non-ascii characters in the answer."
    default_user = f"IT IS NOT A LETTER, IT IS A QUESTION TO BE ANSWER. The writing style for the answer should be stricly be {qa_writing_style}."

    if prompts:
        sys_part = prompts.get("QA_SYSTEM_PROMPT", default_sys)
        user_part = prompts.get("QA_USER_PROMPT", default_user)
        default_qa_sys = f"{sys_part}\n{user_part}\nThe writing style for the answer should be strictly {qa_writing_style}."
    else:
        default_qa_sys = f"You are an expert Software Developer, given the Candidate resume; job description and provided question write a response to that question. Answer as if your are the candidate and you are answering the question. Make the answer short. Do not include any non-ascii characters in the answer. IT IS NOT A LETTER, IT IS A QUESTION TO BE ANSWER. The writing style for the answer should be stricly be {qa_writing_style}."

    if "qa_sys_prompt" not in st.session_state:
        st.session_state.qa_sys_prompt = default_qa_sys
        
    qa_sys_prompt = st.text_area("**Question Prompt**", height=200, value=st.session_state.qa_sys_prompt)
    st.session_state.qa_sys_prompt = qa_sys_prompt
    return st.session_state.qa_sys_prompt


def upload_qns():
    if "qn_text" not in st.session_state:
        st.session_state.qn_text = "No question selected, provide a question first"
    
    with st.form("upload_qn"):
        qn_input = st.text_area("**Paste Question Here (Include Company Name)**", height=68, value="")
        submit = st.form_submit_button("Upload Question")
        
    # after clicking the submit button
    if submit:
        st.session_state.qn_text = qn_input
        st.success("Question saved!")

    return st.session_state.qn_text
    