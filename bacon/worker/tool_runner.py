
import yaml
import os
import subprocess
from pathlib import Path
from bacon.worker.tool_defs import ToolsConfig
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

class ToolRunner:
    def __init__(self, tool_config_path: str = "bacon/config/tools.yaml"):
        self.tools = self._load_tools(tool_config_path)

    def _load_tools(self, config_path):
        with open(config_path, "r") as f:
            config_data = yaml.safe_load(f)
        
        # Validate the config data with Pydantic
        validated_config = ToolsConfig(**config_data)
        
        # Return a dictionary for easy lookup
        return {tool.name: tool for tool in validated_config.tools}

    def run_tool(self, tool_name: str, auto_approve: bool = False, work_dir: str = ".", **kwargs):

        with tracer.start_as_current_span("run_tool") as span:
            span.set_attribute("tool_name", tool_name)
            if tool_name not in self.tools:
                return f"Error: Tool '{tool_name}' not found."

            tool = self.tools[tool_name]

            if tool.requires_approval and not auto_approve:
                print(f"Tool: {tool.name}")
                print(f"Description: {tool.description}")
                print(f"Parameters: {kwargs}")
                approval = input("Do you want to run this tool? (yes/no): ")
                if approval.lower() != 'yes':
                    return "Tool execution skipped by user."

            # Dispatch to the correct handler
            if tool.handler == "api_handler":
                return self.api_handler(tool, **kwargs)
            elif tool.handler == "cli_handler":
                return self.cli_handler(tool, work_dir=work_dir, **kwargs)
            else:
                return f"Error: Unknown handler '{tool.handler}' for tool '{tool_name}'."

    def api_handler(self, tool, **kwargs):
        import requests # Import here to keep it optional

        api_key = None
        if tool.config.api_key_env:
            api_key = os.getenv(tool.config.api_key_env)
            if not api_key:
                return f"Error: API key '{tool.config.api_key_env}' not found in environment."

        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        # Basic parameter validation
        params = {}
        for p_def in tool.config.params:
            if p_def.required and p_def.name not in kwargs:
                return f"Error: Missing required parameter '{p_def.name}'"
            if p_def.name in kwargs:
                params[p_def.name] = kwargs[p_def.name]

        try:
            response = requests.get(tool.config.base_url, headers=headers, params=params)
            response.raise_for_status() # Raise an exception for bad status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            return f"Error making API request: {e}"

    def _sanitize_filepath(self, filepath: str, work_dir: Path) -> Path:
        # Ensure the path is relative and within the working directory
        # This is a critical security measure to prevent directory traversal
        abs_work_dir = work_dir.resolve()
        abs_filepath = (work_dir / filepath).resolve()

        if not abs_filepath.is_relative_to(abs_work_dir):
            raise ValueError("Filepath traversal detected.")
        
        return Path(filepath)

    def cli_handler(self, tool, work_dir, **kwargs):
        command = list(tool.config.command) # Make a copy
        
        # This is a simplified work_dir for now.
        # In a real scenario, this would be the task-specific directory.
        work_dir = Path(work_dir).resolve()
        work_dir.mkdir(parents=True, exist_ok=True)

        for param in tool.config.params:
            if param.name in kwargs:
                value = kwargs[param.name]
                if param.type == "filepath":
                    try:
                        sanitized_path = self._sanitize_filepath(value, work_dir)
                        command.append(str(sanitized_path))
                    except ValueError as e:
                        return f"Error: {e}"
                else:
                    command.append(str(value))
        
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True, # Raise exception on non-zero exit code
                shell=False, # CRITICAL for security
                cwd=work_dir.resolve()
            )
            return result.stdout
        except FileNotFoundError:
            return f"Error: Command not found: {command[0]}"
        except subprocess.CalledProcessError as e:
            return f"Error executing command: {e.stderr}"
        except Exception as e:
            return f"An unexpected error occurred: {e}"

if __name__ == '__main__':
    runner = ToolRunner()
    
    # Test API tool (will fail without a real API key)
    print("--- Testing API Tool ---")
    # Mock the environment variable for the test
    os.environ["BRAVE_API_KEY"] = "dummy_key"
    print(runner.run_tool("search_web", q="BACON agent"))
    del os.environ["BRAVE_API_KEY"]


    # Test CLI tool
    print("\n--- Testing CLI Tool ---")
    print(runner.run_tool("read_file", filename="test.txt"))

    # Test file traversal
    print("\n--- Testing File Traversal ---")
    print(runner.run_tool("read_file", filename="../../../../../etc/passwd"))
