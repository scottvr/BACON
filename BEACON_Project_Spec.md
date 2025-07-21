# 🧠 Project Specification: Bicameral Cognitive Agent (Codename: BEACON)

**B**icameral  
**E**xecutive  
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

- [ ] Plan/Act separation (Executive ⇄ Worker)
- [ ] Modular orchestration layer (LangGraph or custom)
- [ ] Tool execution layer (CLI, Python, APIs)
- [ ] Substrate feedback (psutil, Prometheus, etc.)
- [ ] Long-term memory (vector DB or document store)
- [ ] Working memory / context (chat + task memory)
- [ ] JSON/YAML agent flow config
- [ ] Prompt-driven agent self-reflection and replanning

---

## 🧱 4. System Components

| Component                | Tech Stack / Notes                                               |
|--------------------------|------------------------------------------------------------------|
| Executive Cortex         | OpenAI / Claude + ReAct + DSPy / LangGraph planner              |
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
- [ ] Build Executive ⇄ Worker interaction pattern (ReAct + LangGraph)
- [ ] Integrate tool-use via LangChain or custom function router
- [ ] Implement code synthesis with subprocess feedback
- [ ] Add working memory (in-memory context history)

### Phase 2: Substrate Awareness
- [ ] Add system metric polling (RAM, CPU, disk, GPU if available)
- [ ] Feed metrics into planning decisions
- [ ] Allow Executive to adapt plan based on constraints

### Phase 3: Persistent Memory + Reflection
- [ ] Plug in vector DB for long-term recall (via RAG)
- [ ] Enable self-reflection after tasks (“What did I learn?”)
- [ ] Store toolchains, patterns, and successful code snippets

### Phase 4: Interface and Orchestration
- [ ] Configurable task flows via YAML
- [ ] Web CLI or terminal-based interface
- [ ] Optional streamlit or web dashboard

---

## 📄 7. Example Use Case (Test Scenario)

> Task: “Sort a 100GB CSV file on a machine with 4 cores and 8GB RAM without OOM errors.”

1. Executive plans high-level strategy (chunk, sort, merge).
2. Worker generates chunking script and estimates RAM.
3. Substrate awareness checks available memory.
4. Plan is revised to process in smaller slices.
5. Code is written, tested, executed.
6. Result is validated, memory released.
7. Plan, lessons, and tools are saved to long-term memory.

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
└── README.md
```

---

## 🔮 9. Future Enhancements

- Self-upgrading toolchain (auto-saves working solutions as reusable tools)
- Agent-to-agent collaboration
- Plugin manager for sandboxed skill/module extension
- Trust and introspection layer (self-audit)