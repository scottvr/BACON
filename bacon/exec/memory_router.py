# crumb: exec\memory_router.py

def memory_router(state):
    """
    Router function for memory.
    """
    print("Executing memory_router.")
    last_message = state["messages"][-1]
    if "knowledge" in last_message or "examples" in last_message:
        return "retriever"
    else:
        return "worker"
