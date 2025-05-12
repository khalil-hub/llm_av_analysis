import os
import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

def get_API_key():
    # First: check if key is already available (for local/dev use)
    local_key = os.getenv("OPENAI_API_KEY")

    if local_key:
        return OpenAI(openai_api_key=local_key)

    # If not, ask the user for their key via Streamlit
    user_key = st.text_input("🔑 Enter your OpenAI API key", type="password")
    if user_key:
        return OpenAI(openai_api_key=user_key)
    return None  # Neither key found nor entered

def incident_summary(llm):
    prompt = PromptTemplate(
        input_variables=["log"],
        template="""
    You are an autonomous vehicle safety analyst. The following is a driving log of an autonomous vehicle.
    Each row represents a moment in time, with the following fields:

    - timestamp
    - speed_kph
    - brake_engaged
    - object_detected
    - gps_location

    Your job is to analyze the sequence of events and summarize what happened in clear human language.

    Driving Log:
    {log}
    """
    )
    chain = prompt | llm
    return chain

def run_summary(av_string, chain):
    return chain.invoke({"log": av_string})


