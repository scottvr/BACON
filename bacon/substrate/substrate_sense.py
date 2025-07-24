from bacon.substrate.metrics import get_system_metrics
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

def substrate_sense(state):
    """
    Gets system metrics and adds them to the state.
    """
    with tracer.start_as_current_span("substrate_sense") as span:
        metrics = get_system_metrics()
        span.set_attribute("metrics", str(metrics))
        return {"messages": [{"substrate": metrics}]}