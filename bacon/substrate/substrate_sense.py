from bacon.substrate.metrics import get_system_metrics

def substrate_sense(state):
    """
    Gets system metrics and adds them to the state.
    """
    metrics = get_system_metrics()
    return {"messages": [{"substrate": metrics}]}