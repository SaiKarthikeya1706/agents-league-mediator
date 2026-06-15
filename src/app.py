import sys
import os
import streamlit as st
from dotenv import load_dotenv
import pandas as pd
from pypdf import PdfReader
from pptx import Presentation

# --- Path Injection Fix ---
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_path not in sys.path:
    sys.path.append(root_path)

from src.main import run_agent 

# --- Setup & Config ---
load_dotenv()
st.set_page_config(page_title="Mediator & Logic Engine", layout="wide", page_icon="🛡️")

# --- Helper: Text Extraction ---
def get_file_text(file):
    text = f"\n--- Source: {file.name} ---\n"
    try:
        if file.type == "application/pdf":
            reader = PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ""
        elif "excel" in file.type or "spreadsheet" in file.type:
            df = pd.read_excel(file)
            text += df.to_string()
        elif "powerpoint" in file.type or "presentation" in file.type:
            prs = Presentation(file)
            for slide in prs.slides:
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        text += shape.text + "\n"
        else:
            text += file.getvalue().decode("utf-8", errors="ignore")
    except Exception as e:
        text += f"[Error reading file: {e}]"
    return text

# --- Session State ---
if "messages" not in st.session_state: st.session_state.messages = []

def main():
    st.markdown("<h1>🛡️ Mediator & Logic Engine</h1>", unsafe_allow_html=True)
    st.caption("Autonomous Policy Arbitration & Universal Reasoning System")

    # Render Chat History
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])
    
    # Unified Chat Input
    if user_query := st.chat_input("Ask about company policy, team performance, or general research..."):
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"): st.markdown(user_query)
        
        with st.chat_message("assistant"):
            with st.spinner("Agent is reasoning..."):
                try:
                    file_context = ""
                    # 1. Check for User Uploads
                    if "uploaded_files" in st.session_state and st.session_state.uploaded_files:
                        for file in st.session_state.uploaded_files:
                            file_context += get_file_text(file)
                        st.info("Using **Custom Uploaded** context.")
                    # 2. Fallback to Default Data
                    else:
                        with open("data/policy.txt", "r") as f:
                            file_context += f"\n--- Policy Context ---\n{f.read()}"
                        with open("data/synthetic_learners.json", "r") as f:
                            file_context += f"\n--- Performance Context ---\n{f.read()}"
                        st.warning("No files uploaded. Using **Default System Context**.")
                    
                    # Execution
                    result = run_agent(user_query, context=file_context)
                    
                    with st.expander("🔍 Reasoning Trace & Observability"):
                        st.write(f"**Targeted Path:** {result['path'].upper()}")
                        st.write(f"**Orchestration Status:** Success")
                    
                    st.markdown(result['content'])
                    st.session_state.messages.append({"role": "assistant", "content": result['content']})
                except Exception as e:
                    st.error(f"Execution Error: {e}")
        st.rerun()

    # Sidebar Controls
    with st.sidebar:
        st.markdown("## ⚙️ CONTROL ARRAY")
        
        st.write("📦 **Pre-loaded Knowledge:**")
        st.caption("✅ `policy.txt`")
        st.caption("✅ `synthetic_learners.json`")
        st.divider()
        
        st.session_state.uploaded_files = st.file_uploader(
            "Upload Custom Docs (Overrides Defaults)", 
            accept_multiple_files=True, 
            type=['pdf', 'xlsx', 'xls', 'pptx', 'ppt', 'txt']
        )
        st.divider()
        st.success("Foundry/Fabric/Work IQ Integrated")
        if st.button("Clear Conversation"):
            st.session_state.messages = []
            st.rerun()

if __name__ == "__main__":
    main()