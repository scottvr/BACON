
import subprocess
import uuid
import os
import shutil
from pathlib import Path

class CodeExecutor:
    def __init__(self, timeout: int = 60, memory_limit: str = "1g", cpus: str = "1.5"):
        self.timeout = timeout
        self.memory_limit = memory_limit
        self.cpus = cpus
        self.run_id = str(uuid.uuid4())
        self.stage_dir = Path(f"output/runs/{self.run_id}")
        self.stage_dir.mkdir(parents=True, exist_ok=True)

    def execute(self, code: str, input_files: list = None):
        # 1. Stage files
        with open(self.stage_dir / "main.py", "w") as f:
            f.write(code)

        if input_files:
            for file_path in input_files:
                if Path(file_path).exists():
                    shutil.copy(file_path, self.stage_dir)

        # 2. Build Docker command
        docker_command = [
            "docker", "run",
            "--rm",
            "--network=none",
            f"--memory={self.memory_limit}",
            f"--cpus={self.cpus}",
            "--read-only",
            "-v", f"{self.stage_dir.resolve()}:/app:rw",
            "--user", f"{os.getuid()}:{os.getgid()}",
            "--cap-drop=ALL",
            "bacon-executor:latest"
        ]

        # 3. Execute and monitor
        try:
            result = subprocess.run(
                docker_command,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            stdout = result.stdout
            stderr = result.stderr
            exit_code = result.returncode
        except subprocess.TimeoutExpired:
            stdout = ""
            stderr = "Execution timed out."
            exit_code = -1 # Custom code for timeout

        # 4. Harvest results (placeholder)
        output_files = [str(f) for f in self.stage_dir.glob("*") if f.name != "main.py"]

        return {
            "stdout": stdout,
            "stderr": stderr,
            "exit_code": exit_code,
            "output_files": output_files
        }

if __name__ == '__main__':
    # Example Usage
    executor = CodeExecutor()
    test_code = "print('Hello from the sandbox!')"
    execution_result = executor.execute(code=test_code)
    print(execution_result)
