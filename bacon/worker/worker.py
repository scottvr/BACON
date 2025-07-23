from bacon.worker.tool_runner import ToolRunner

def worker(state):
    # For now, we'll execute a hardcoded tool call.
    # Later, this will come from the planner.
    tool_name = "read_file"
    params = {"filename": "test.txt"}
    
    runner = ToolRunner()
    result = runner.run_tool(
        tool_name, 
        auto_approve=state.get("auto_approve", False),
        work_dir=state.get("constraints", {}).get("work_dir", "."),
        **params
    )
    
    return {"messages": [f"tool_output: {result}"]}





