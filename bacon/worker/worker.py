# crumb: worker\worker.py
from bacon.worker.code_executor import run_python_code

def worker(state):
    """
    Worker node function.
    """
    print("Executing worker node.")
    # For now, we'll just execute a simple python script.
    code = "print('Hello from the worker!')"
    result = run_python_code(code)
    return {"messages": [result]}