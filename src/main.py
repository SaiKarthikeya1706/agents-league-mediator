import os
import json
import operator
from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv

load_dotenv()

# --- 1. State Definition ---
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    next_step: str

# --- 2. Data Loading Helpers ---
def load_policy():
    """Reads the latest policy from the data folder."""
    try:
        with open("data/policy.txt", "r") as f:
            return f.read()
    except FileNotFoundError:
        return "Policy documentation currently unavailable."

def load_insights_data():
    """Reads synthetic learner data for the Insights Agent."""
    try:
        with open("data/synthetic_learners.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# --- 3. Nodes ---
def router_node(state: AgentState):
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    last_message = state['messages'][-1].content
    
    # Responsible AI / Safety Check
    if any(word in last_message.lower() for word in ["pii", "password", "secret", "private"]):
        return {"next_step": "safety_error"}

    prompt = f"""
    Analyze the request: "{last_message}"
    Classify the intent into one of these three categories: 'policy', 'search', or 'insights'.
    - 'policy': Involves company rules, discount requests, or compliance procedures.
    - 'search': General knowledge or web queries.
    - 'insights': Team performance, learning data, or manager reports.
    Return ONLY the category name.
    """
    decision = llm.invoke([SystemMessage(content="You are an intelligent router."), HumanMessage(content=prompt)]).content.strip().lower()
    return {"next_step": decision}

def policy_node(state: AgentState):
    """Foundry IQ Pattern: Grounded Policy Arbitration"""
    user_input = state['messages'][-1].content
    policy_data = load_policy()
    
    system_prompt = f"You are the Corporate Policy Mediator. Use the following policy to answer the request: {policy_data}"
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    response = llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=user_input)])
    return {"messages": [HumanMessage(content=response.content)]}

def search_node(state: AgentState):
    """General Reasoning Node"""
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    response = llm.invoke(state['messages'][-1].content)
    return {"messages": [HumanMessage(content=response.content)]}

def insights_node(state: AgentState):
    """Fabric IQ Pattern: Semantic Analysis of Structured Data"""
    data = load_insights_data()
    prompt = f"""
    You are the Manager Insights Agent. Analyze the following team performance data: {json.dumps(data)}.
    Summarize team readiness and recommend one improvement action for the manager.
    """
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"messages": [HumanMessage(content=response.content)]}

def safety_node(state: AgentState):
    """Responsible AI Fallback"""
    return {"messages": [HumanMessage(content="I'm sorry, I cannot process this request as it involves sensitive information or potential security risks.")]}

# --- 4. Graph Assembly ---
workflow = StateGraph(AgentState)

workflow.add_node("router", router_node)
workflow.add_node("policy", policy_node)
workflow.add_node("search", search_node)
workflow.add_node("insights", insights_node)
workflow.add_node("safety_error", safety_node)

workflow.set_entry_point("router")

def should_continue(state: AgentState):
    return state['next_step']

workflow.add_conditional_edges(
    "router", 
    should_continue, 
    {
        "policy": "policy", 
        "search": "search", 
        "insights": "insights",
        "safety_error": "safety_error"
    }
)

workflow.add_edge("policy", END)
workflow.add_edge("search", END)
workflow.add_edge("insights", END)
workflow.add_edge("safety_error", END)

app = workflow.compile()

# --- 5. Execution Interface ---
def run_agent(user_query: str):
    """Interface for the Streamlit App"""
    # Invoke the LangGraph app
    final_state = app.invoke({"messages": [HumanMessage(content=user_query)]})
    
    return {
        "content": final_state['messages'][-1].content,
        "path": final_state.get('next_step', 'Unknown')
    }