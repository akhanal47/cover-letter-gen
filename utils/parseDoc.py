import os
import tempfile
from pathlib import Path
import streamlit as st
import PyPDF2
from docx import Document
from openai import OpenAI
from fpdf import FPDF
import re

def save_uploaded_file(uploaded_file):
    suffix = Path(uploaded_file.name).suffix
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp.write(uploaded_file.getbuffer())
    tmp.close()
    return tmp.name

def parse_pdf(path):
    text = ""
    reader = PyPDF2.PdfReader(path)
    for page in reader.pages:
        if (t := page.extract_text()):
            text += t
    return text

def parse_docx(path):
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs)

def upload_resume_jd():
    if "resume_text" not in st.session_state:
        st.session_state.resume_text = "No resume selected, please ask the user to provide a resume before writing the Cover Letter"
    if "jd" not in st.session_state:
        st.session_state.jd = " "
    if "file_name" not in st.session_state:
        st.session_state.file_name = "No Name.pdf"

    with st.form("upload_form"):
        uploaded_file = st.file_uploader("**Select Resume File**", type=["pdf", "docx"])
        jd_input = st.text_area("**Paste Job Description Here**", height=300, value=st.session_state.jd)
        submit = st.form_submit_button("Upload Resume & JD")

    if submit:
        st.session_state.jd = jd_input
        st.success("Resume and JD uploaded successfully!")
        if uploaded_file:
            file_name = uploaded_file.name
            path = save_uploaded_file(uploaded_file)
            resume_text = parse_pdf(path) if path.lower().endswith(".pdf") else parse_docx(path)
            st.session_state.resume_text = resume_text
            st.session_state.file_name = file_name.split(".")[0]
            os.unlink(path)
        else:
            st.warning("Please upload a PDF or DOCX file.")

    return st.session_state.resume_text, st.session_state.jd, st.session_state.file_name