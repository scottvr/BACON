# crumb: exec\feedback_loop.py
run_count = 0

def feedback_loop(state):
    """
    Feedback loop node function.
    """
    global run_count
    print("Executing feedback_loop node.")
    if run_count > 0:
        return {"messages": ["halt"]}
    run_count += 1
    return {"messages": ["continue"]}