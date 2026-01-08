import os
import tempfile
from pathlib import Path
import streamlit as st
import PyPDF2
from docx import Document
from openai import OpenAI
from fpdf import FPDF
import re
import json

def load_prompts_from_file():
    current_dir = os.path.dirname(__file__)
    filepath = os.path.join(current_dir, "prompt.json")
    
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading prompt.json: {e}")
    return None

def letter_system_prompt(letter_writing_style):
    prompts = load_prompts_from_file()

    default_sys = "You are an expert cover letter writer, given the Candidate Details and job description, Write a cover letter for the candidate. The cover letter should highlight candidate strength in lue of the job description. Strictly follow the instructions and the writing style provided"
    default_user = "Write the best possible cover letter for the mentioned job descripton based on the mentioned resume. Make the letter verbose, detailed and professional but not too long. The cover letter should be structured in the following format, first line should be salutation, second line should be the subject, third line should be the body of the letter, divided into two paragraphs, and the last line should be the closing, followed by exit greeting and candidate name in the next line which is present in the candidate details. Provide the cover letter in plain text letter format, which can be copied and pasted into a word document without editing. There needs to a blank line between each line. The body can be single or two paragraphs at maximum. PLEASE, DO NOT HAVE ANY PLACEHOLDER TEXT IN THE LETTER. Make the letter as human as possible"

    if prompts:
        sys_part = prompts.get("SYSTEM_PROMPT", "")
        user_part = prompts.get("USER_PROMPT", "")
        
        default_val = f"{sys_part}\n\n{user_part}\n\nThe writing style should be strictly {letter_writing_style}"
    else:
        default_val = f"{default_sys}\n\n{default_user}\n\nThe writing style should be strictly {letter_writing_style}"

    if "sys_prompt" not in st.session_state:
        st.session_state.sys_prompt = default_val

    sys_prompt = st.text_area("**System Prompt**", height=250, value=st.session_state.sys_prompt)
    st.session_state.sys_prompt = sys_prompt
    return sys_prompt

# construct the prompt for the llm, this will be used to generate the cover lette
def create_prompt(resume_text, jd, sys_prompt):
    # load the resume and job description from session state
    resume_text = st.session_state.resume_text
    jd = st.session_state.jd
    prompt = f"""
    {sys_prompt}
    \n\n Candidate Details: \n {resume_text}
    \n\n Job Description: \n {jd}
    """
    return prompt

def create_qa_prompt(resume_text, jd, question, sys_prompt):
    # load the resume and job description from session state
    resume_text = st.session_state.resume_text
    jd = st.session_state.jd
    prompt = f"""
    {sys_prompt}
    \n\n Candidate Details: \n {resume_text}
    \n\n Job Description: \n {jd}
    \n\n Question: \n {question}
    """
    return prompt


class llmResponse:
    @staticmethod
    def api_response(sys_prompt, main_prompt, apiKey, model_name, temp):
        # use openai format for future compatibility
        client = OpenAI(api_key=apiKey,
                        base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
        api_response = client.chat.completions.create(
                    model=model_name,
                    temperature=temp,
                    n=1,
                    messages=[
                        {"role": "system", "content": f"{sys_prompt}"},
                            {
                                "role": "user",
                                "content": f"{main_prompt}"
                            }
                        ]
                    )
        return api_response.choices[0].message.content
