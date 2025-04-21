import os
import tempfile
from pathlib import Path
import streamlit as st
import PyPDF2
from docx import Document
from openai import OpenAI
from fpdf import FPDF
import re

# read the api key from user or env file, if not provided by user
def get_api_key():
    default_key = os.getenv("GEMINI_KEY")
    with st.form("api_key_form"):
        apiKey = st.text_input(
            "Enter API key",
            key="api_input"
        )
        submitted = st.form_submit_button("Save API Key")
    if submitted:
        if apiKey:
            st.session_state.apiKey = apiKey
        else:
            st.session_state.apiKey = default_key
            st.warning("Please enter a valid API key; for now a default key is used.")
    return st.session_state.get("apiKey", default_key)

# select the LLM to use, only Gemini is supported for now
def get_llm_provider():
    provider = st.selectbox(
        "Select LLM to use",
        ["Gemini"],  # placeholder list
        index=0,
        key="llm_provider"
    )

    # for gemini, allow some model options
    if provider == "Gemini":
        model_name = st.selectbox(
            "Select Gemini Model",
            ["gemini-2.5-pro-exp-03-25", "gemini-2.0-flash-exp-image-generation", "gemini-2.0-flash-exp", "gemini-2.0-pro-exp-02-05"],
            index=0,
            key="gemini_model"
        )
        st.session_state.model_name = model_name
        return provider, model_name

    # set state vars
    st.session_state.provider = provider
    return provider, None
