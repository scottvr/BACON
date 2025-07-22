# crumb: exec\feedback_loop.py
def feedback_loop(state):
    """
    Feedback loop node function.
    """
    if "tool_output: hello world" in state["messages"]:
        return {"messages": ["halt"]}
    return {"messages": ["continue"]}