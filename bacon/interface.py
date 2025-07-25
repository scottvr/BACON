import yaml
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

from bacon.exec.planner import planner
from bacon.worker.worker import worker
from bacon.exec.feedback_loop import feedback_loop
from bacon.exec.memory_router import memory_router
from bacon.worker.tools.retriever import retriever
from bacon.substrate.substrate_sense import substrate_sense

class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    auto_approve: bool

from dotenv import load_dotenv
from bacon.memory.snapshot import save_snapshot, load_snapshot
from pathlib import Path

load_dotenv()

class BaconAgent:
    # Python API for the BACON agent
    def __init__(self, config_path: str = "bacon/langgraph_bacon.yaml", recursion_limit: int = 15):
        self.config_path = config_path
        self.recursion_limit = recursion_limit
        self._load_graph()

    def _load_graph(self):
        with open(self.config_path, "r") as f:
            config = yaml.safe_load(f)

        self.workflow = StateGraph(AgentState)
        node_functions = {
            "planner": planner,
            "worker": worker,
            "feedback_loop": feedback_loop,
            "memory_router": lambda state: state,
            "retriever": retriever,
            "substrate_sense": substrate_sense,
        }

        for node in config["nodes"]:
            func = node_functions.get(node["id"], lambda state: state)
            self.workflow.add_node(node["id"], func)

        self.workflow.set_entry_point(config["entry_point"])
        for edge in config["edges"]:
            if edge["from"] == "memory_router":
                continue
            self.workflow.add_edge(edge["from"], edge["to"])

        self.workflow.add_conditional_edges(
            "feedback_loop",
            lambda state: END,
            {END: END}
        )

        self.graph = self.workflow.compile()

    def run(self, task: str, constraints: dict = None, auto_approve: bool = False) -> AgentState:
        # Execute the agent on a given task and return the final state
        snapshot_path = Path("bacon_snapshot.pkl")
        if snapshot_path.exists():
            initial_state = load_snapshot(snapshot_path)
            print("Resuming from snapshot.")
        else:
            initial_messages = [f"task: {task}"]
            if constraints:
                for k, v in constraints.items():
                    initial_messages.append(f"{k}: {v}")
            initial_state = {"messages": initial_messages, "auto_approve": auto_approve}

        final_state = self.graph.invoke(initial_state, {"recursion_limit": self.recursion_limit})
        print(f"Final state: {final_state}")
        return final_state
