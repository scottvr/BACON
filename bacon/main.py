import argparse
from bacon.interface import BaconAgent

def main():
    parser = argparse.ArgumentParser(description="BACON Agent CLI")
    parser.add_argument("task", help="Task description for the agent")
    parser.add_argument("--config", default="langgraph_bacon.yaml", help="Path to LangGraph YAML config")
    parser.add_argument("--recursion", type=int, default=15, help="Recursion limit for the agent")
    args = parser.parse_args()

    agent = BaconAgent(config_path=args.config, recursion_limit=args.recursion)
    result = agent.run(args.task)
    print("=== BACON Agent Result ===")
    for msg in result["messages"]:
        print(msg)

if __name__ == "__main__":
    main()