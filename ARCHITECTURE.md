
# Orchestration Service Architecture

<p align="center">
  <b>High-Level Architecture Diagram</b><br>
  <i>This diagram shows the strict boundaries of orchestration-svc: only orchestration logic, API, and interfaces/ports live here. All business logic, adapters, and integrations are externalized for maximum modularity and testability.</i>
</p>

---

```mermaid
%% alt: Orchestration-svc boundaries: only orchestration logic, API, and ports. All adapters/integrations are external.
graph TD
    Client["Client / API Consumer"]
    subgraph orchestration-svc (this repo)
        APILayer["1️⃣ API Layer (FastAPI)"]
        Engine["2️⃣ Orchestration Engine"]
        Ports["3️⃣ Ports / Interfaces"]
    end
    subgraph External Services
        Adapter1["Adapter: Workflow Repo"]
        Adapter2["Adapter: Domain Logic"]
        Adapter3["Adapter: Integrations"]
    end
    Client -->|"Request"| APILayer
    APILayer -->|"Dispatch"| Engine
    Engine -->|"Invoke"| Ports
    Ports -.->|"Contract"| Adapter1
    Ports -.->|"Contract"| Adapter2
    Ports -.->|"Contract"| Adapter3
```

<p align="center"><i>Request flow: <b>1️⃣ API Layer</b> → <b>2️⃣ Orchestration Engine</b> → <b>3️⃣ Ports</b> → <b>External Adapters</b></i></p>


---

**orchestration-svc (this repo):**
- Only orchestration logic, API, and interfaces/ports. No business logic, adapters, or integrations.
- All contracts (ports/interfaces) are public and versioned.
- Maximum testability and modularity by design.

**External Services:**
- All adapters, domain models, and integrations are implemented outside this repo.
- Adapters implement the contracts (ports) defined in orchestration-svc.

---

---

<sub>This diagram is generated with <a href="https://mermaid-js.github.io/mermaid/#/">Mermaid</a> and is accessible for screen readers via alt text.</sub>
