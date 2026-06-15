# System Architecture: Mediator & Logic Engine

## 1. Architectural Overview
The Mediator & Logic Engine is built on a **Stateful Orchestration Pattern** using LangGraph. The core design principle is **decoupling**: we isolate knowledge (Data Layer), reasoning (Agent Nodes), and context (Router/State).


## 2. Agent Logic Flow
The system operates as a finite state machine. The `router_node` determines the path, and the state dictionary (`AgentState`) maintains the conversation history and decision trail.

```mermaid
graph TD
    %% Nodes representing Agents and Logic Nodes
    subgraph Orchestration ["Mediator & Logic Engine (LangGraph)"]
        RouterNode{"Router Agent<br/>(Contextual Router)"}
        PolicyAgent["Policy Mediator Agent"]
        LogicAgent["General Research Agent"]
        InsightsAgent["Performance Insights Agent"]
        SafetyAgent["Safety/Guardrail Agent"]
    end

    %% Integration with Microsoft IQ Layers
    subgraph IQ_Layers ["Microsoft Intelligence Layers"]
        WorkIQ["Work IQ<br/>(Work Context & Routing)"]
        FoundryIQ["Foundry IQ<br/>(RAG Policy Grounding)"]
        FabricIQ["Fabric IQ<br/>(Performance Data Analytics)"]
    end

    %% User Flow
    User((User Input)) -->|Intent Analysis| RouterNode
    
    %% Routing Logic with IQ Mappings
    RouterNode -->|PII/Risk Detected| SafetyAgent
    RouterNode -->|Policy Inquiry| WorkIQ
    WorkIQ --> RouterNode
    
    RouterNode -->|Route| PolicyAgent
    PolicyAgent <-->|query_knowledge_base| FoundryIQ
    
    RouterNode -->|Route| LogicAgent
    LogicAgent <-->|search_discovery| FoundryIQ
    
    RouterNode -->|Route| InsightsAgent
    InsightsAgent <-->|semantic_analysis| FabricIQ

    %% End Path
    PolicyAgent --> Final(Final Response)
    LogicAgent --> Final
    InsightsAgent --> Final
    SafetyAgent --> Final

    %% Styling for sophistication
    classDef agent fill:#f0f7ff,stroke:#0078d4,stroke-width:2px;
    classDef iq fill:#fef3e7,stroke:#d97706,stroke-width:2px;
    classDef route fill:#f5f5f5,stroke:#333,stroke-width:2px;
    
    class PolicyAgent,LogicAgent,InsightsAgent,SafetyAgent agent;
    class WorkIQ,FoundryIQ,FabricIQ iq;
    class RouterNode route;
```


## 3. IQ Layer Integration Deep-Dive

### Foundry IQ (Policy Grounding)
The `policy_node` does not rely on LLM training data. It utilizes a **RAG-lite pattern** where the `policy.txt` file is injected into the system prompt context at runtime. This ensures the model treats the policy as the absolute source of truth.

### Fabric IQ (Business Logic)
The `insights_node` performs **Semantic Reasoning**. By passing the structured `synthetic_learners.json` (a JSON object) into the LLM, we allow the agent to treat "Role," "Status," and "Readiness" as **first-class entities** rather than simple text tokens.

### Work IQ (Contextual Awareness)
The `router_node` functions as the **Cognitive Gatekeeper**. It uses an LLM-based classifier to map user intent into specific execution paths, ensuring that sensitive requests or complex queries are handled by the appropriate specialized node.

## 4. Design Decisions

* **State Management:** We use `Annotated[List[BaseMessage], operator.add]` within LangGraph. This ensures that every node in the graph has access to the full conversation context (Chat History) without needing to manually pass session data.
* **Safety Fallback:** The safety check is placed at the **entry point** (The Router). By intercepting potentially sensitive inputs *before* they hit the specialized reasoning nodes, we reduce the blast radius of any "hallucination" or "prompt injection" risks.
* **Modularity:** Each agent node is designed as a standalone function. This makes it trivial to swap the `search_node` for a more complex tool-calling agent (e.g., Tavily Search) in the future without refactoring the core graph.