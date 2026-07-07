# 🛡️ Mediator & Logic Engine
### Autonomous Enterprise Arbitration Framework

![Mediator & Logic Engine Logo](assets/agents_AI.jpg)

[![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![LangGraph](https://img.shields.io/badge/Orchestration-LangGraph-1c3d5a)](https://www.langchain.com/langgraph)
[![Gemini](https://img.shields.io/badge/LLM-Gemini%202.5%20Flash-4285F4?logo=google)](https://ai.google.dev/)
[![Vector Store](https://img.shields.io/badge/Vector%20Store-Chroma-orange)](https://www.trychroma.com/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-ff4b4b?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit%20Cloud-brightgreen)](https://agents-league-mediator.streamlit.app/)

---

## 🧠 Challenge Submission
**Track:** Reasoning Agents with Microsoft Foundry
**Project Objective:** A dual-purpose analytical platform combining strict organizational policy arbitration (**The Mediator**) with a **5-agent autonomous enterprise framework** for real-time information discovery, dynamic document analysis, and complex problem-solving — grounded in a real, vector-based retrieval pipeline rather than raw context stuffing.

---

## ⚖️ The Problem
In modern enterprise environments, requests (such as sales discounts) often lead to friction between departments. Manual, human-in-the-loop approvals are slow, inconsistent, and suffer from "precedent creep." Furthermore, most agents lack the ability to bridge the gap between static policy and real-time business data analysis, and many "RAG" implementations quietly skip retrieval entirely, just dumping full documents into the prompt.

## 🚀 Our Solution
The **Mediator & Logic Engine** is a durable, Python-based orchestration framework built with **LangGraph**. It replaces manual gatekeeping with an autonomous **Reasoning Engine** that:

1. **Dynamic Context Ingestion** — Users upload PDFs, Excel sheets, PPTs, or TXT files directly through the UI; the engine adapts its knowledge base in real time.
2. **Policy Mediator (Foundry IQ Pattern)** — Grounds every ruling using genuine **retrieval-augmented generation**: the policy corpus is chunked, embedded, and indexed in a vector store, then queried by similarity search at inference time — not stuffed wholesale into the prompt.
3. **Universal Logic Engine (Reasoning & Orchestration)** — LangGraph drives durable, multi-step reasoning loops: `Router → Policy / Search / Insights → Response`.
4. **Data-Driven Insights (Fabric IQ Pattern)** — Analyzes structured performance data directly, giving manager-level insights without forcing structured data through a chunking pipeline it doesn't need.

---

## 🛠️ Technical Architecture & IQ Mapping

| Microsoft IQ Layer | Our Implementation | Technical Purpose |
| :--- | :--- | :--- |
| **Foundry IQ** | `policy_node` — Chroma vector store + Gemini embeddings | Grounds policy rulings via top-k similarity search over indexed source documents |
| **Fabric IQ** | `insights_node` — Structured JSON analysis | Analyzes structured team performance data directly (full-context, no chunking needed) |
| **Work IQ** | `router_node` — Contextual routing | Classifies intent and routes to the correct agent node |

### Retrieval Pipeline (the part that makes this *actually* RAG)

policy.txt ──► RecursiveCharacterTextSplitter (800 chars, 100 overlap)
──► Gemini embeddings (gemini-embedding-001)
──► Chroma vector store (persisted, pre-indexed at build time)
User query ──► embed query ──► similarity_search(k=4) ──► top-k relevant chunks
──► passed to Gemini 2.5 Flash


User-uploaded documents get the same treatment via an ephemeral, session-scoped Chroma index — built once per upload, queried the same way, never persisted, so nothing sensitive lingers after the session ends.

## Architecture Diagram:

```mermaid
graph TD
    subgraph Inputs ["Data Inputs"]
        User((User Query))
        UserDocs[("Dynamic Files<br/>(PDF, XLSX, PPTX, TXT)")]
    end

    subgraph Orchestration ["Mediator & Logic Engine (LangGraph)"]
        RouterNode{"Router Agent<br/>(Contextual Router)"}
        PolicyAgent["Policy Mediator Agent"]
        LogicAgent["General Research Agent"]
        InsightsAgent["Performance Insights Agent"]
        SafetyAgent["Safety/Guardrail Agent"]
    end

    subgraph Retrieval ["Vector Retrieval Layer"]
        Embed["Gemini Embeddings<br/>(gemini-embedding-001)"]
        VectorDB[("Chroma Vector Store<br/>(chunked & indexed)")]
    end

    subgraph IQ_Layers ["Microsoft Intelligence Layers"]
        WorkIQ["Work IQ<br/>(Contextual Routing)"]
        FoundryIQ["Foundry IQ<br/>(RAG Policy Grounding)"]
        FabricIQ["Fabric IQ<br/>(Performance Analytics)"]
    end

    User -->|Intent Analysis| RouterNode
    UserDocs -->|Ephemeral Index| VectorDB

    RouterNode -->|PII/Risk Detected| SafetyAgent
    RouterNode -->|Policy Inquiry| WorkIQ
    WorkIQ --> RouterNode

    RouterNode -->|Route| PolicyAgent
    PolicyAgent <-->|similarity_search top-k| VectorDB
    VectorDB <-->|embed| Embed
    PolicyAgent <-->|grounded generation| FoundryIQ

    RouterNode -->|Route| LogicAgent
    LogicAgent <-->|search_discovery| FoundryIQ

    RouterNode -->|Route| InsightsAgent
    InsightsAgent <-->|semantic_analysis| FabricIQ

    PolicyAgent --> Final(Final Response)
    LogicAgent --> Final
    InsightsAgent --> Final
    SafetyAgent --> Final

    classDef agent fill:#f0f7ff,stroke:#0078d4,stroke-width:2px;
    classDef iq fill:#fef3e7,stroke:#d97706,stroke-width:2px;
    classDef route fill:#f5f5f5,stroke:#333,stroke-width:2px;
    classDef input fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,stroke-dasharray: 5 5;
    classDef vector fill:#fff0f6,stroke:#c2185b,stroke-width:2px;

    class PolicyAgent,LogicAgent,InsightsAgent,SafetyAgent agent;
    class WorkIQ,FoundryIQ,FabricIQ iq;
    class RouterNode route;
    class UserDocs input;
    class Embed,VectorDB vector;
```

---

## 📊 Key Features
* **Real Vector-Based RAG** — Chroma + Gemini embeddings, not context-stuffing dressed up as retrieval.
* **Multi-Format Support** — Seamlessly processes PDF, XLSX, PPTX, and TXT files via an intuitive sidebar uploader.
* **Autonomous Router** — Automatically classifies requests and selects the best agent for the task.
* **Observability** — Built-in Reasoning Traces in the UI let you monitor the agent's logic flow in real time.
* **Ephemeral User-Upload Indexing** — Session-scoped vector index for uploaded docs; nothing persists after you close the tab.

---

## 🛡️ Responsible AI & Security
* **Input Guardrails** — A proactive `safety_node` intercepts PII/credential-related requests at the router level, before they ever reach a reasoning node.
* **Secrets Hygiene** — API keys live exclusively in `.env` (gitignored) locally and in Streamlit Cloud's Secrets manager in production; never committed, never hardcoded. Git history has been scrubbed of any prior exposure.
* **Fictional Sample Data** — The pre-loaded `policy.txt` and `synthetic_learners.json` are illustrative, not real company data — clearly labeled as such in the UI.
* **Production Ready** — Architected to transition to **Azure Key Vault** and **Managed Identities** for enterprise-grade secrets management.

---

## 🏠 User Interface & Experience

* **Unified Control Array** — A sidebar "Command Center" for uploading custom policy/performance documents, clearing conversation history, and verifying active intelligence layers.
* **Transparent Reasoning** — Every response ships with a Reasoning Trace expander showing which path the router took and which IQ layer was consulted.
* **Interactive Context Awareness** — Real-time feedback on whether you're grounded in default or custom-uploaded context.

![Mediator & Logic Engine](assets/home.png)

---

## 📸 Demonstration of Capabilities

* **Contextual Policy Arbitration** — Cross-references retrieved policy chunks to answer complex business rules regarding contract terms.
![Mediator & Logic Engine](assets/Policy.png)

* **Proactive Safety Guardrails** — Automatically detects and blocks requests involving sensitive PII or security risks.
![Mediator & Logic Engine](assets/security.png)

* **Boundary-Aware Logic** — Maintains strict adherence to retrieved context, refusing to hallucinate outside the provided policy domain.
![Mediator & Logic Engine](assets/Boundary-Aware.png)

---

## ❓ Frequently Asked Questions

### 1. How is this different from standard chatbots like ChatGPT or Gemini?
Standard AI tools operate as "black boxes" relying on broad, static training data. The Mediator & Logic Engine is a **durable, enterprise-grade framework**: every response is traced back to a specific, retrieved chunk of your policy or data via LangGraph's deterministic execution path, minimizing hallucination and preserving auditability.

### 2. Why use this instead of a simple RAG application?
Most "RAG" demos skip the "R" — they just paste an entire document into the prompt and call it retrieval. This engine performs **real retrieval**: documents are chunked, embedded with Gemini's embedding model, indexed in Chroma, and queried via similarity search at inference time, returning only the top-k relevant chunks. On top of that retrieval layer sits an **Active Arbitrator** — a Work IQ router for intent classification, Safety Guardrails for risk interception, and a Fabric IQ layer for structured-data reasoning that doesn't need chunking at all.

### 3. How secure is my data within this system?
Sensitive requests are intercepted by `safety_node` at the router level before reaching any reasoning node. API keys are never hardcoded or committed — they're managed via `.env` locally (gitignored) and Streamlit Cloud Secrets in production, with a documented path to Azure Key Vault and Managed Identities for enterprise deployment.

### 4. Can I use this for departments outside Sales and HR?
Yes — Dynamic Context Ingestion makes the system domain-agnostic. Upload HR handbooks, IT security protocols, legal compliance documents, or technical specs, and the vector index adapts instantly with zero code changes.

### 5. What makes the Reasoning Trace feature important?
In an enterprise setting, "yes" or "no" isn't enough — you need to know *why*. The Reasoning Trace reveals which IQ layer was consulted, which retrieved chunk triggered the decision, and what path the router took, giving the transparency corporate governance requires.

---

## 🔗 Project Quick Links

| Resource | Link |
| :--- | :--- |
| **Source Code** | [GitHub Repository](https://github.com/SaiKarthikeya1706/agents-league-mediator) |
| **Live Demonstration** | [Streamlit App](https://agents-league-mediator.streamlit.app/) |

---

## ⚙️ Quick Start Guide

```bash
# 1. Clone the repository
git clone https://github.com/SaiKarthikeya1706/agents-league-mediator
cd agents-league-mediator

# 2. Set up environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure your API key
echo "GOOGLE_API_KEY=your_key_here" > .env

# 5. Build the vector index (one-time, or whenever policy.txt changes)
python -m src.ingest

# 6. Launch the application
streamlit run src/app.py
```

> **Note:** Step 5 is required before first run — it builds the Chroma vector store that grounds every policy query. If you update `data/policy.txt`, re-run `python -m src.ingest` to refresh the index.

---

## 🧪 Tech Stack

`LangGraph` · `Google Gemini 2.5 Flash` · `Gemini Embeddings (gemini-embedding-001)` · `Chroma` (via `langchain-chroma`) · `Streamlit` · `PyPDF` · `python-pptx` · `pandas`