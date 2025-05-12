import os
import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool  # if we add tools later
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

def check_safety_rules(log_text: str) -> str:
    """
    Analyzes the AV driving log and returns whether the vehicle violated basic safety rules:
    - Did it stop at red light?
    - Did it engage brakes when a pedestrian was detected?
    - Did it drive too fast in rain?
    """
    violations = []
    rows = log_text.strip().split("\n\n")  # assume each row is an event
    
    for row in rows:
        if "traffic_signal: red" in row.lower() and "brakes engaged: false" in row.lower():
            violations.append("🚨 Did not brake at red light.")
        if "object detected: pedestrian" in row.lower() and "brakes engaged: false" in row.lower():
            violations.append("🚨 Pedestrian detected but no braking.")
        if "weather condition: rain" in row.lower():
            speed_str = row.split("the car was going at ")[1].split(" kph")[0]
            if float(speed_str) > 30:
                violations.append(f"⚠️ Speed too high in rain: {speed_str} kph")

    return "Rule violations:\n" + "\n".join(violations) if violations else "✅ No rule violations found."

def suggest_mitigation(log_text: str) -> str:
    """
    Suggests ways to improve safety based on observed patterns in the driving log.
    """
    suggestions = []
    if "rain" in log_text.lower():
        suggestions.append("🔧 Reduce speed and increase braking sensitivity in rainy conditions.")
    if "manual_override" in log_text.lower():
        suggestions.append("🔧 Improve AV reliability to avoid manual overrides during critical events.")
    if "pedestrian" in log_text.lower() and "brakes engaged: false" in log_text.lower():
        suggestions.append("🔧 Upgrade pedestrian detection and automatic braking response.")

    return "Mitigation suggestions:\n" + "\n".join(suggestions) if suggestions else "✅ No immediate improvements identified."

def create_incident_agent(llm):
    tools = [
        Tool(
            name="check safety rules",
            func=check_safety_rules,
            description="checks the safety rules"
        ),
        Tool(
            name="suggest mitigation",
            func=suggest_mitigation,
            description="Suggests ways to improve safety based on observed patterns"
        )
    ]
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    return agent

def run_agent(av_string, agent):
    prompt = f"""
    You are an expert AV accident analyst. Use the driving log below to answer:
    - What caused the incident?
    - Was it the vehicle’s fault?
    - What could have prevented it?
    You have also the tools at your disposal.

    Log:
    {av_string}
    """

    return agent.run(prompt)
