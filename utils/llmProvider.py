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
import requests
from datetime import timedelta

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
            st.warning("Please enter a valid API key; for now a default GEMINI key is used.")
    return st.session_state.get("apiKey", default_key)

def get_temperature():
    temperature = st.slider("**Creativity:**", 0.0, 2.0, 0.7, 0.1)  # random temp between 0 and 2 for each run
    st.session_state.temperature = temperature
    return temperature

def get_writing_style():
    writing_style = st.selectbox(
        "**Select Letter Style**",
        ["professional", "sarcastic", "technical", "formal", "semi-formal", "creative", "persuasive", "humorous", "friendly"],
        index=2
    )
    st.session_state.writing_style = writing_style
    return st.session_state.writing_style

def get_qa_writing_style():
    qa_writing_style = st.selectbox(
        "**Select Qns Ans Style**",
        ["professional", "sarcastic", "technical", "formal", "semi-formal", "creative", "persuasive", "humorous", "friendly"],
        index=1
    )
    st.session_state.qa_writing_style = qa_writing_style
    return st.session_state.qa_writing_style

# select the LLM to use, only Gemini is supported for now
def get_llm_provider():
    model_map = get_model_data()
    provider_list = list(model_map.keys())

    provider = st.selectbox(
        "Select LLM to use",
        provider_list,  # get's from gist
        index=0,
        key="llm_provider"
    )

    current_models = model_map.get(provider, [])

    model_name = st.selectbox(
        f"Select {provider} Model",
        current_models,
        index=0,
        key="gemini_model"
    )

    # Set state vars
    st.session_state.provider = provider
    st.session_state.model_name = model_name
    
    return provider, model_name

@st.cache_data(ttl=timedelta(days=10))
def get_model_data():
    gist_url = "https://gist.githubusercontent.com/akhanal47/fd3eebb886053eee44f95735b4b9b848/raw/d8a3511fde4f08993066c09b0eb7254d24ae5211/free_apis.json"
    
    # fallback
    fallback_data = {
        "Gemini": ["gemini-2.5-flash-preview-04-17", "gemini-2.0-flash-exp-image-generation", "gemini-2.0-flash-exp", "gemini-2.0-pro-exp-02-05"]
    }

    try:
        response = requests.get(gist_url)
        if response.status_code == 200:
            data = response.json()
            return {item['provider']: item['model_names'] for item in data}
    except Exception as e:
        return fallback_data