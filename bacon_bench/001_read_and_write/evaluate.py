

import sys
from pathlib import Path

def main():
    # The script will be run from the root of the project,
    # so the path to the files needs to be relative to that.
    task_dir = Path("bacon_bench/001_read_and_write")
    input_file = task_dir / "input.txt"
    output_file = task_dir / "output.txt" # This is where the agent should write the file

    if not output_file.exists():
        print("FAIL: Output file 'output.txt' does not exist.")
        sys.exit(1)

    input_content = input_file.read_text()
    output_content = output_file.read_text()

    if input_content == output_content:
        print("PASS: Output file content matches input file content.")
        sys.exit(0)
    else:
        print("FAIL: Output file content does not match input file content.")
        print(f"Expected:\n---\n{input_content}\n---")
        print(f"Got:\n---\n{output_content}\n---")
        sys.exit(1)

if __name__ == "__main__":
    main()

