# Mediator AI: Enterprise Policy Arbitration Framework

## The Problem
Sales and Finance often clash over discount requests. Human-in-the-loop approvals are slow, inconsistent, and prone to "precedent creep."

## Our Solution
An autonomous **Multi-Agent Arbitration Framework** that:
1. **Retrieves** current company policy (Grounded RAG).
2. **Evaluates** requests against financial constraints (GPT-4o/Gemini Logic).
3. **Enforces** governance by mandating documentation (Business Cases, Contract terms).

## Tech Stack
* **Orchestration:** LangChain
* **LLM:** Gemini 2.5 Flash
* **Governance:** Custom Policy Injection (RAG)
* **Environment:** Python 3.9+ / Virtual Environment