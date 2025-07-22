# crumb: exec\feedback_loop.py
def feedback_loop(state):
    """
    Feedback loop node function.
    """
    # Temporary halt condition for testing the executor
    for message in state["messages"]:
        if isinstance(message, str) and message.startswith("tool_output"):
            return {"messages": ["halt"]}
    return {"messages": ["continue"]}