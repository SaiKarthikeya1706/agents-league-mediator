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
    context: str  # Added context to state

# --- 3. Nodes (Updated to use State Context) ---
def router_node(state: AgentState):
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    last_message = state['messages'][-1].content
    
    if any(word in last_message.lower() for word in ["pii", "password", "secret", "private"]):
        return {"next_step": "safety_error"}

    prompt = f"""
    Analyze the request: "{last_message}"
    Classify intent: 'policy', 'search', or 'insights'.
    Return ONLY the category name.
    """
    decision = llm.invoke([SystemMessage(content="You are an intelligent router."), HumanMessage(content=prompt)]).content.strip().lower()
    return {"next_step": decision}

def policy_node(state: AgentState):
    """Grounded Policy Arbitration using injected context"""
    user_input = state['messages'][-1].content
    # Use context passed from Streamlit, falling back to local files if empty
    context = state.get('context', "")
    
    system_prompt = f"""You are the Corporate Policy Mediator. 
    Use the following information to answer the request. If the info is in the provided User Uploads, prioritize it:
    {context}
    """
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    response = llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=user_input)])
    return {"messages": [HumanMessage(content=response.content)]}

def search_node(state: AgentState):
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    # Even search node can benefit from context if the user asks about the doc
    prompt = f"Use this context to inform your answer: {state.get('context', '')}\n\nQuery: {state['messages'][-1].content}"
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"messages": [HumanMessage(content=response.content)]}

def insights_node(state: AgentState):
    prompt = f"""
    You are the Manager Insights Agent. 
    Analyze the following data: {state.get('context', '')}
    Summarize team readiness and recommend one improvement action.
    """
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"messages": [HumanMessage(content=response.content)]}

def safety_node(state: AgentState):
    return {"messages": [HumanMessage(content="I'm sorry, I cannot process this request as it involves sensitive information.")]}

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

workflow.add_conditional_edges("router", should_continue, {
    "policy": "policy", "search": "search", "insights": "insights", "safety_error": "safety_error"
})
workflow.add_edge("policy", END); workflow.add_edge("search", END); 
workflow.add_edge("insights", END); workflow.add_edge("safety_error", END)

app = workflow.compile()

# --- 5. Execution Interface (Updated) ---
def run_agent(user_query, context=""):
    """Interface for the Streamlit App"""
    # Pass context into the graph state
    final_state = app.invoke({
        "messages": [HumanMessage(content=user_query)],
        "context": context
    })
    
    return {
        "content": final_state['messages'][-1].content,
        "path": final_state.get('next_step', 'Unknown')
    }