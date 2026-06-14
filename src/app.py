import streamlit as st
import os
from main import run_agent 
from dotenv import load_dotenv

# --- Setup & Config ---
load_dotenv()
st.set_page_config(
    page_title="Mediator & Logic Engine", 
    layout="wide", 
    page_icon="🛡️"
)

# --- Session State ---
if "messages" not in st.session_state: 
    st.session_state.messages = []

def main():
    # Header Section
    st.markdown("<h1>🛡️ Mediator & Logic Engine</h1>", unsafe_allow_html=True)
    st.caption("Autonomous Policy Arbitration & Universal Reasoning System")

    # Render Chat History
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): 
            st.markdown(msg["content"])
    
    # Unified Chat Input
    if user_query := st.chat_input("Ask about company policy, team performance, or general research..."):
        # Display User Message
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"): 
            st.markdown(user_query)
        
        # Agent Processing (The LangGraph Orchestrator)
        with st.chat_message("assistant"):
            with st.spinner("Agent is reasoning..."):
                try:
                    # Capture the result which contains path and content
                    result = run_agent(user_query)
                    
                    # 1. Visualization: Reasoning Trace (Crucial for Challenge Submission)
                    with st.expander("🔍 Reasoning Trace & Observability"):
                        st.write(f"**Targeted Path:** {result['path'].upper()}")
                        st.write(f"**Orchestration Status:** Success")
                        st.write(f"**Agent Framework:** LangGraph")
                    
                    # 2. Display the final answer
                    st.markdown(result['content'])
                    
                    # Save to state
                    st.session_state.messages.append({"role": "assistant", "content": result['content']})
                
                except Exception as e:
                    st.error(f"Execution Error: {e}")
        
        # Force rerun to update UI
        st.rerun()

    # Sidebar Controls
    with st.sidebar:
        st.markdown("## ⚙️ CONTROL ARRAY")
        st.info("Status: LangGraph Orchestration Active")
        st.divider()
        st.write("**IQ Intelligence Layers:**")
        st.success("Foundry IQ: Policy Grounding")
        st.success("Fabric IQ: Semantic Analysis")
        st.success("Work IQ: Contextual Routing")
        st.divider()
        if st.button("Clear Conversation"):
            st.session_state.messages = []
            st.rerun()

if __name__ == "__main__":
    main()