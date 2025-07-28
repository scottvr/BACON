from bacon.worker.tool_runner import ToolRunner

def worker(state):
    # The planner should have produced a tool call.
    tool_call = state["messages"][-1]
    tool_name = tool_call["name"]
    params = tool_call["arguments"]
    
    runner = ToolRunner()
    result = runner.run_tool(
        tool_name, 
        **params
    )
    
    return {"messages": [f"tool_output: {result}"]}
    #





