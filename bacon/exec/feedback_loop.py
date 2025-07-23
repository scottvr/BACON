# crumb: exec\feedback_loop.py
def feedback_loop(state):
    """
    Feedback loop node function.
    """
    # Check for a tool output anywhere in the messages to decide to halt.
    # This is more robust against parallel nodes modifying the state.
    for message in reversed(state["messages"]):
        if isinstance(message, str) and message.startswith("tool_output"):
            return {"messages": ["halt"]}
    return state