from bacon.worker.code_executor import CodeExecutor

def worker(state):
    # For now, we'll execute a hardcoded piece of code.
    # Later, this will come from the planner.
    code_to_execute = "print('Executing code from the worker!')"
    
    executor = CodeExecutor()
    result = executor.execute(code=code_to_execute)
    
    return {"messages": [f"tool_output: {result}"]}