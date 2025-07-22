# Project Specification: Bicameral Cognitive Agent (Codename: BACON)

**B**icameral   
**A**gent with   
**C**ompute-aware  
**O**rchestration and  
**N**avigation

---

## 📌 1. Objective

Build a modular, substrate-aware cognitive agent system with a bicameral architecture. It will:
- Separate high-level reasoning (Executive) from task execution (Worker).
- Support tool use, code synthesis, and recursive planning.
- Monitor its own runtime environment (CPU, memory, I/O, GPU).
- Adapt plans dynamically based on system constraints.
- Persist long-term and working memory across sessions.
- Be composable from current open-source tools and LLM APIs.

---

## 📍 2. Problem Statement

Existing LLM agents are monolithic or brittle. They lack:
- Architecture-level separation between planning and execution.
- Awareness of the environment they run in (compute, storage, etc).
- The ability to revise goals and methods based on runtime observations.
- Continuity across sessions via persistent memory.
- An integrated feedback loop between cognition and substrate.

---

## ✅ 3. Goals (MVP)

- [x] Plan/Act separation (Executive ⇄ Worker)
- [x] Modular orchestration layer (LangGraph or custom)
- [ ] Tool execution layer (CLI, Python, APIs)
- [ ] Substrate feedback (psutil, Prometheus, etc.)
- [ ] Long-term memory (vector DB or document store)
- [x] Working memory / context (chat + task memory)
- [x] JSON/YAML agent flow config
- [ ] Prompt-driven agent self-reflection and replanning

---

## 🧱 4. System Components

| Component                | Tech Stack / Notes                                               |
|--------------------------|------------------------------------------------------------------|
| High-Level Planner / Meta-Controller  | OpenAI / Claude + ReAct + DSPy / LangGraph planner              |
| Worker / Actuator Agent  | Code executor (OpenInterpreter, subprocess), API tools          |
| Orchestration Layer      | LangGraph, FastAPI for LLM calls + function routing             |
| Tool Invocation Layer    | LangChain Tools, CLI runner, HTTP plugin runner                 |
| Substrate Awareness      | `psutil`, Prometheus client, custom sensors                     |
| Working Memory           | LangChain memory, Redis or ephemeral JSON store                 |
| Long-Term Memory         | Chroma / Weaviate / FAISS + metadata index                      |
| RAG Engine               | LlamaIndex / DSPy / LangChain Retriever                         |
| Persistence Layer        | SQLite / JSON file for context snapshots                        |
| UI (Optional)            | CLI interface, Jupyter agent shell, or simple streamlit panel   |

---

## 🚧 5. Non-Goals (MVP)

- Real-world robotics/actuation
- Model fine-tuning or RLHF loops
- Fully autonomous self-expansion
- Multi-agent collaboration (but should plan for later)

---

## 🛠 6. Development Roadmap (MVP)

### Phase 1: Core Loop and Skeleton
- [x] Build Executive ⇄ Worker interaction pattern (ReAct + LangGraph)
- [x] Integrate tool-use via LangChain or custom function router
- [ ] Approval mechanism for tool execution (e.g., "Do you want to run this code?") In a tool's definition (tools.yaml), add a flag like requires_approval: true.. When the agent wants to use such a tool (e.g., execute_code, spend_money), it pauses and waits for user confirmation via the CLI. 
- [x] Code Executor sandboxing (Docker container for code_executor.py)
- [ ] Implement code synthesis with subprocess feedback
- [x] Add working memory (in-memory context history)

### Phase 2: Substrate Awareness
- [ ] Add system metric polling (RAM, CPU, disk, GPU if available)
- [ ] Feed metrics into planning decisions
- [ ] Allow Executive to adapt plan based on constraints
- [ ] Integrate observability via LangSmith traces and OpenTelemetry metrics for substrate and tool feedback
- [ ] The agent should track the cost of its LLM calls (input_tokens * price + output_tokens * price).
- [ ] A task can be given a max_budget constraint (e.g., constraints={"RAM": "8GB", "budget": "$5.00"}).
- [ ] The Executive planner should be aware of the remaining context window size and use summarization or context compression techniques to avoid failures on long-running tasks.

### Phase 3: Persistent Memory + Reflection
- [ ] Plug in vector DB for long-term recall (via RAG)
- [ ] Enable self-reflection after tasks (“What did I learn?”)
- [ ] Store toolchains, patterns, and successful code snippets
- [ ] Track Prompt strategy variants(e.g., executive tone, persona conditioning)
- [ ] Track model-specific tuning quirks
- [ ] Memory slotting/Recall strategies (e.g., by task type, tool used, or outcome)
- [ ] snapshot the entire state of the LangGraph execution graph, not just the memory.
After each step, save the current state (including all node inputs/outputs, memory, and the current position in the graph) to a database like SQLite or a file.
When the agent starts, it can check for an incomplete run and offer to resume from the last saved state. This makes the system resilient to failures.

### Phase 4: Interface and Orchestration
- [ ] Configurable task flows via YAML
- [ ] Web CLI or terminal-based interface
- [ ] Optional streamlit or web dashboard


### Evaluation and Testing Framework
- [ ] Create a simple test suite of tasks (a "BACON-bench"). These could be a dozen scenarios like the CSV sorting example.
- [ ] Define success metrics for each test (e.g., task completion, resource usage, cost, number of steps).
- [ ] Run this evaluation suite automatically after major changes to measure progress and catch regressions. You can even use a cheaper, faster LLM (like Haiku or Llama 3 8B) to "judge" the quality of the final output.

###  Dynamic Tool & Prompt Library
- After a successful task, the Reflection step should identify if any generated code or sequence of tool calls is useful.
- The agent could then be prompted to write a docstring and function signature for that code, and automatically save it as a new tool in its library (e.g., as a new .py file or a new entry in a tool database). This is the foundation for the "self-upgrading toolchain" listed in future enhancements and is achievable within the MVP.
---

## 📄 7. Example Use Case (Test Scenario)

Task: “Sort a 100GB CSV file on a machine with 4 cores and 8GB RAM without OOM errors.”

Goal: "Sort the 100GB CSV file."

Constraints: Max RAM usage of 7GB, completion within 30 minutes.

**BACON's Process:**

- **Plan:** The Meta-Controller selects a "sort-large-file" strategy. The default is an external merge sort.
- **Substrate Query:** It queries the Substrate Monitor: "Available RAM = 8GB; Available Cores = 4."
- **Constraint Analysis:** It calculates that a naive implementation might spike memory usage above the 7GB constraint. It refines the plan: "Use a memory-mapped file or process the file in N chunks of size S, where S is calculated to keep peak RAM usage below 7GB."
- **Action:** The Code Synthesis worker generates a Python script using pandas with a specific chunksize.
- **Monitoring & Adaptation:** During execution, the Substrate Monitor reports that I/O is the bottleneck. The Meta-Controller might revise the plan again to launch parallel processes to handle I/O and computation concurrently, if the cores allow.
---

## 📚 8. Repo Structure (Proposed)

```
beacon/
├── main.py                  # entry point CLI or server
├── exec/
│   ├── planner.py           # high-level LLM task planner
│   └── memory.py            # working + long-term memory
├── worker/
│   ├── tool_runner.py       # API/CLI tool execution
│   └── code_executor.py     # sandboxed Python/exec env
├── substrate/
│   └── metrics.py           # psutil/Prometheus polling
├── memory/
│   ├── vector_store.py      # RAG backends
│   └── snapshot.py          # session state
├── config/
│   ├── agents.yaml          # plan/worker routing logic
│   └── tools.yaml           # registered tools
|── prompts/
│   └── executive_prompts.md # LLM prompts
|   └── self_reflection.md   # LLM prompts 
|   └── code_generator.md    # LLM prompts
└── README.md
```

---

## 🔮 9. Future Enhancements

- Self-upgrading toolchain (auto-saves working solutions as reusable tools)
- Agent-to-agent collaboration
- Plugin manager for sandboxed skill/module extension
- Trust and introspection layer (self-audit)

## 10. Usage Interface

CLI Example:
```bash
python -m bacon.main "Sort a 100GB CSV with 8GB RAM limit"
```

Python API Example:
```python
from bacon.interface import BaconAgent

agent = BaconAgent(config_path="bacon/langgraph_bacon.yaml")
result = agent.run("Sort a 100GB CSV under 8GB RAM", constraints={"RAM": "8GB"})
```

Input:
Natural language task, optional constraints dictionary.

Output:
A dictionary including:

Plan steps

Tool invocations

Code artifacts (optional paths)

Final task state/messages

