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
from utils.qnAnswers import *

# load the environment variables
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env")


def main():
    ### These should be on the left side of the app
    with st.sidebar:
        provider, model_name = get_llm_provider()   # a provider is always selected
        apiKey = get_api_key()
        temperature = get_temperature()
        writing_style = get_writing_style()
        qa_writing_style = get_qa_writing_style()
        sys_prompt = letter_system_prompt(writing_style)
        qa_sys_prompt = question_sys_prompt(qa_writing_style)
    
        # set the state variables
        st.session_state.provider = provider
        st.session_state.apiKey = apiKey
        st.session_state.sys_prompt = sys_prompt
        st.session_state.model_name = model_name
        st.session_state.temperature = temperature
        st.session_state.qa_sys_prompt = qa_sys_prompt

    #------ Main App window -------
    resume_text, jd, candidate_name = upload_resume_jd()
    main_prompt = create_prompt(resume_text, jd, sys_prompt)    # get the full prompt to generate cover letter
    
    # set states, to cache for the session, resume text & jd already set in respective func
    st.session_state.main_prompt = main_prompt  


    # call the LLM and get the cover letter, this should happen only when the user clicks the button
    if st.button("Generate Cover Letter"):    
        cover_letter = llmResponse.api_response(st.session_state.sys_prompt, 
                                                   st.session_state.main_prompt, 
                                                   st.session_state.apiKey, 
                                                   st.session_state.model_name, 
                                                   st.session_state.temperature)
        st.session_state.cover_letter = cover_letter

    if "cover_letter" in st.session_state:
        if "downable_cov_letter" not in st.session_state:
            st.session_state.downable_cov_letter = st.session_state.cover_letter
        
        # the user can directly edit the generated text, before downloading
        st.text_area("**Generated Cover Letter:**", height=400, value=st.session_state.cover_letter, key="downable_cov_letter")

        # create pdf and allow download 
        downloadable_pdf_path = create_pdf(st.session_state.downable_cov_letter, candidate_name)
        with open(downloadable_pdf_path, "rb") as f:
            st.download_button("Download Cover Letter", 
                            f.read(), 
                            file_name=f"Cover_Letter_{candidate_name}.pdf", 
                            mime="application/pdf",
                            icon=":material/download:")
    
    # now for the q/a part
    qa_text = upload_qns()
    qa_full_prompt = create_qa_prompt(resume_text, jd, qa_text, qa_sys_prompt)
    st.session_state.qa_full_prompt = qa_full_prompt
    st.session_state.qa_text = qa_text

    # generate answer to qns asked
    if st.button("Answer Question"):
        qa_answer = llmResponse.api_response(st.session_state.qa_sys_prompt, 
                                                st.session_state.qa_full_prompt, 
                                                st.session_state.apiKey, 
                                                st.session_state.model_name, 
                                                st.session_state.temperature)
        st.session_state.qa_answer = qa_answer
        # show answer
        st.text_area("**Answer:**", height=200, value=st.session_state.qa_answer)

if __name__ == "__main__":
    main()

