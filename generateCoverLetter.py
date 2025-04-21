import os
import tempfile
from pathlib import Path
import streamlit as st
import PyPDF2
from docx import Document
from openai import OpenAI
from fpdf import FPDF
import re

from utils.parseDoc import *
from utils.getJd import getJd
from utils.createPdf import *
from utils.llmResponse import *
from utils.llmResponse import llmResponse 
from utils.llmProvider import *

# load the environment variables
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env")


def main():
    ### These should be on the left side of the app
    with st.sidebar:
        provider, model_name = get_llm_provider()   # a provider is always selected
        apiKey = get_api_key()
        sys_prompt = system_prompt()

        # set the state variables
        st.session_state.provider = provider
        st.session_state.apiKey = apiKey
        st.session_state.sys_prompt = sys_prompt
        st.session_state.model_name = model_name

    #------ Main App window -------
    resume_text, jd, candidate_name = upload_resume_jd()
    main_prompt = create_prompt(resume_text, jd, sys_prompt)    # get the full prompt

    # call the LLM and get the cover letter, this should happen only when the user clicks the button
    if st.button("Generate Cover Letter"):    
        cover_letter = llmResponse.gemini_response(sys_prompt, main_prompt, apiKey, model_name)
        st.session_state.cover_letter = cover_letter

        # the user can directly edit the generated text, before downloading
        downable_cov_letter = st.text_area("**Generated Cover Letter**", height=400, value=cover_letter)
        st.session_state.downable_cov_letter = downable_cov_letter

        # create pdf and allow download 
        downloadable_pdf_path = create_pdf(cover_letter, candidate_name)
        with open(downloadable_pdf_path, "rb") as f:
            st.download_button("Download Cover Letter", 
                            f.read(), 
                            file_name=f"Cover_Letter_{candidate_name}.pdf", 
                            mime="application/pdf",
                            icon=":material/download:")

if __name__ == "__main__":
    main()

