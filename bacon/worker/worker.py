from bacon.worker.tool_runner import ToolRunner

def worker(state):
    # The planner should have produced a tool call.
    tool_call = state["messages"][-1]
    tool_name = tool_call["tool"]
    params = tool_call["params"]
    
    runner = ToolRunner()
    work_dir = state.get("constraints", {}).get("work_dir", ".")
    result = runner.run_tool(
        tool_name, 
        auto_approve=state.get("auto_approve", False),
        work_dir=work_dir,
        **params
    )
    
    return {"messages": [f"tool_output: {result}"]}
    #





