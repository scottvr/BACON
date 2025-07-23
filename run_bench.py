
import subprocess
import json
from pathlib import Path

def run_benchmark(task_dir: Path):
    print(f"--- Running Benchmark: {task_dir.name} ---")
    
    # 1. Read the task definition
    task_file = task_dir / "task.json"
    with open(task_file, "r") as f:
        task_data = json.load(f)
    prompt = task_data["prompt"]

    # 2. Run the agent
    # For now, we assume the agent knows where to find the files.
    # A more robust solution would involve passing the working directory.
    print(f"Running agent with prompt: '{prompt}'")
    agent_process = subprocess.run(
        ["python3", "-m", "bacon.main", prompt],
        capture_output=True,
        text=True
    )
    
    if agent_process.returncode != 0:
        print("Agent execution failed.")
        print(agent_process.stderr)
        return "FAIL"

    print("Agent execution complete.")

    # 3. Run the evaluation script
    eval_script = task_dir / "evaluate.py"
    print("Running evaluation...")
    eval_process = subprocess.run(
        ["python3", str(eval_script)],
        capture_output=True,
        text=True
    )

    print(eval_process.stdout)
    if "FAIL" in eval_process.stdout:
        return "FAIL"
    else:
        return "PASS"

def main():
    bench_dir = Path("bacon_bench")
    results = {}

    for task_dir in sorted(bench_dir.iterdir()):
        if task_dir.is_dir() and (task_dir / "task.json").exists():
            result = run_benchmark(task_dir)
            results[task_dir.name] = result

    print("\n--- Benchmark Summary ---")
    for name, result in results.items():
        print(f"{name}: {result}")

if __name__ == "__main__":
    main()
