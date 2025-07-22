from bacon.worker.code_executor import CodeExecutor

def worker(state):
    # For now, we'll execute a hardcoded piece of code.
    # Later, this will come from the planner.
    code_to_execute = "print('Executing code from the worker!')"
    
    print(f"Code to execute:\n---\n{code_to_execute}\n---")
    approval = input("Do you want to run this code? (yes/no): ")
    
    if approval.lower() == 'yes':
        executor = CodeExecutor()
        result = executor.execute(code=code_to_execute)
        return {"messages": [f"tool_output: {result}"]}
    else:
        return {"messages": ["tool_output: execution skipped by user."]}

