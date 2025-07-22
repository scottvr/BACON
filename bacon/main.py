import yaml
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

from bacon.exec.planner import planner
from bacon.worker.worker import worker
from bacon.exec.feedback_loop import feedback_loop
from bacon.exec.memory_router import memory_router
from bacon.memory.retriever import retriever
from bacon.substrate.substrate_sense import substrate_sense

class AgentState(TypedDict):
    messages: Annotated[list, operator.add]

def main():
    """
    Main entry point for the BACON agent.
    """
    with open("langgraph_bacon.yaml", "r") as f:
        config = yaml.safe_load(f)

    workflow = StateGraph(AgentState)

    node_functions = {
        "planner": planner,
        "worker": worker,
        "feedback_loop": feedback_loop,
        "memory_router": lambda state: state,
        "retriever": retriever,
        "substrate_sense": substrate_sense,
        "observability_tracer": lambda state: state,
    }

    for node in config["nodes"]:
        workflow.add_node(node["id"], node_functions[node["id"]])

    workflow.set_entry_point(config["entry_point"])

    for edge in config["edges"]:
        if edge["from"] == "memory_router":
            continue
        workflow.add_edge(edge["from"], edge["to"])

    workflow.add_conditional_edges(
        "memory_router",
        memory_router,
        {
            "retriever": "retriever",
            "worker": "worker",
        }
    )

    workflow.add_conditional_edges(
        "feedback_loop",
        lambda state: "planner" if state["messages"][-1] != "halt" else END,
        {"planner": "planner", END: END}
    )

    graph = workflow.compile()

    print("BACON agent graph compiled successfully.")
    print("Running the graph...")
    initial_state = {"messages": ["start"]}
    final_state = graph.invoke(initial_state, {"recursion_limit": 15})
    print(f"Final state: {final_state}")

if __name__ == "__main__":
    main()