import os
import tempfile
from pathlib import Path
import streamlit as st
import PyPDF2
from docx import Document
from openai import OpenAI
from fpdf import FPDF
import re

def system_prompt():
    default = (
        "You are an expert cover letter writer, given the Candidate Details and job description, "
        "Write a cover letter for the candidate. The cover letter should highlight candidate strength in lue of the job description. "
        "Make the letter verbose, detailed and professional but not too long. "
        "The cover letter should be structured in the following mannger, first line should be salutation, second line should be the subject, third line should be the body of the letter, and the last line should be the closing, followed by exit greeting and candidate name in the next line which is present in the candidate details. "
        "Provide the cover letter in plain text letter format, which can be copied and pasted into a word document without editing. "
        "There needs to a blank line between each line. "
        "The body should be a single paragraph and should not contain a blank line at all. "
        "Make the letter as human as possible. "
        "PLEASE, DO NOT HAVE ANY PLACEHOLDER TEXT IN THE LETTER. "
    )
    if "system_prompt" not in st.session_state:
        st.session_state.system_prompt = default
    sys_prompt = st.text_area("**System Prompt**", height=350, value=st.session_state.system_prompt)
    st.session_state.system_prompt = sys_prompt
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

class llmResponse:
    @staticmethod
    def gemini_response(sys_prompt, main_prompt, apiKey, model_name):
        # use openai format for future compatibility
        client = OpenAI(api_key=apiKey,
                        base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
        api_response = client.chat.completions.create(
                    model=model_name,
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
