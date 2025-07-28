import argparse
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from bacon.interface import BaconAgent
from bacon.util.output_manager import OutputManager

def main():
    parser = argparse.ArgumentParser(description="BACON Agent CLI")
    parser.add_argument("task", help="Task description for the agent")
    parser.add_argument("--config", default="bacon/langgraph_bacon.yaml", help="Path to LangGraph YAML config")
    parser.add_argument("--recursion", type=int, default=15, help="Recursion limit for the agent")
    parser.add_argument("--auto-approve", action="store_true", help="Auto-approve all tool executions")
    parser.add_argument("--work-dir", type=str, default=".", help="Working directory for the agent")
    args = parser.parse_args()

    agent = BaconAgent(config_path=args.config, recursion_limit=args.recursion)
    result = agent.run(
        args.task, 
        auto_approve=args.auto_approve,
        constraints={"work_dir": "output/runs/current_task"}
    )

    output_mgr = OutputManager()
    task_dir = output_mgr.create_task_dir(task_name=args.task)
    output_mgr.save_messages(task_dir, result["messages"])

    # Optional: if your LLM produces a plan or code artifacts, save those here
    # output_mgr.save_summary(task_dir, {"status": "complete", "task": args.task})

    print("=== BACON Agent Result ===")
    for msg in result["messages"]:
        print(msg)
    print(f"Output saved to: {task_dir}")

if __name__ == "__main__":
    main()