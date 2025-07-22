
import subprocess

def worker(state):
    # Hardcoded tool execution
    result = subprocess.run(["echo", "hello world"], capture_output=True, text=True)
    return {"messages": [f"tool_output: {result.stdout.strip()}"]}
