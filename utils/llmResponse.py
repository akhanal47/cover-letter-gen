import os
import tempfile
from pathlib import Path
import streamlit as st
import PyPDF2
from docx import Document
from openai import OpenAI
from fpdf import FPDF
import re

def letter_system_prompt(letter_writing_style):
    default = f"""You are an expert Java Developer, given the Candidate Details and job description write a cover letter for the candidate.
The cover letter should highlight candidate strength in lieu of the job description.
Make the letter verbose, detailed and professional but not too long. 
The cover letter should be structured in the following mannger, first line should be salutation, second line should be the subject, third line should be the body of the letter, and the last line should be the closing, followed by exit greeting and candidate name in the next line which is present in the candidate details. 
Provide the cover letter in plain text letter format, which can be copied and pasted into a word document without editing. 
There needs to a blank line between each line. 
The body should be a single paragraph and should not contain a blank line at all. 
The cover letter should be as much as humanly written.
PLEASE, DO NOT HAVE ANY PLACEHOLDER TEXT IN THE LETTER.
The writing style should be stricly be {letter_writing_style}"""

    if "letter_system_prompt" not in st.session_state:
        st.session_state.sys_prompt = default
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
    def gemini_response(sys_prompt, main_prompt, apiKey, model_name, temp):
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
