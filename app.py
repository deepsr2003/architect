import streamlit as st
import requests

# Dashboard Configuration
st.set_page_config(page_title="Architect AI Dashboard", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #e0e0e0; }
    .stTextArea textarea { background-color: #161b22; color: white; border: 1px solid #30363d; }
    .stButton button { background-color: #21262d; color: white; border: 1px solid #30363d; width: 100%; }
    .stButton button:hover { background-color: #30363d; border-color: #8b949e; }
    </style>
""", unsafe_allow_html=True)

st.title("Architect: Autonomous System Design Engine")
st.write("Synthetic Engineering for Backend Microservices")

# User Input
project_idea = st.text_area("System Objectives", placeholder="Enter the project requirements and business logic...")

if st.button("Generate System Blueprint"):
    if project_idea:
        with st.spinner("Executing Multi-Agent Orchestration..."):
            try:
                # Backend URL (Update for local/codespace deployment)
                response = requests.get(f"http://localhost:8000/build?project_idea={project_idea}")
                if response.status_code == 200:
                    data = response.json()
                    st.divider()
                    st.markdown("### Formal Engineering Blueprint")
                    st.markdown(data['blueprint'])
                else:
                    st.error("Protocol Error: Backend failed to generate blueprint.")
            except Exception as e:
                st.error(f"Connection Error: {e}")
    else:
        st.warning("Input required: Please define a project context.")