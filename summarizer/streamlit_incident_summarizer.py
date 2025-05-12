import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from summarizer.incident_summarizer import get_API_key, incident_summary, run_summary

st.title("🚗 AV Incident Summarizer")
st.markdown("Enter incident data rows below.")

# Get OpenAI key and model
llm = get_API_key()
if not llm:
    st.warning("Please enter your API key to continue.")
    st.stop()

# Add rows dynamically
if "rows" not in st.session_state:
    st.session_state.rows = []

if st.button("➕ Add New Row"):
    st.session_state.rows.append({"timestamp": "", "speed_kph": "", "brake_engaged": "", "object_detected": "", "gps_location": ""})

log_text = ""
for i, row in enumerate(st.session_state.rows):
    st.write(f"### Row {i + 1}")
    col1, col2 = st.columns(2)
    timestamp = col1.text_input("Timestamp", value=row["timestamp"], key=f"timestamp_{i}")
    speed_kph = col2.number_input("Speed (kph)", value=float(row["speed_kph"] or 0), key=f"speed_{i}")
    brake_engaged = st.selectbox("Brakes Engaged?", [True, False], key=f"brake_{i}")
    object_detected = st.text_input("Object Detected", value=row["object_detected"], key=f"object_{i}")
    gps_location = st.text_input("GPS Location", value=row["gps_location"], key=f"gps_{i}")

    log_text += (
        f"At {timestamp}, the car was going at {speed_kph} kph. "
        f"Brakes engaged: {brake_engaged}. "
        f"Object detected: {object_detected}. "
        f"Location: {gps_location}\n"
    )

if st.button("🧠 Analyze Incident"):
    if log_text.strip():
        with st.spinner("Analyzing..."):
            chain = incident_summary(llm)
            summary = run_summary(log_text, chain)
        st.success("Summary:")
        st.write(summary)
    else:
        st.warning("Please add at least one log row.")
