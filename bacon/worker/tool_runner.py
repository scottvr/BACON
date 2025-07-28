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
        return {tool.function.name: tool for tool in validated_config.tools}

    def run_tool(self, tool_name: str, **kwargs):
        with tracer.start_as_current_span("run_tool") as span:
            span.set_attribute("tool_name", tool_name)
            if tool_name not in self.tools:
                return f"Error: Tool '{tool_name}' not found."

            tool = self.tools[tool_name]

            # For now, we will not support approval for standardized tools.
            # This can be added back later if needed.

            if tool.type == "function":
                return self.function_handler(tool.function, **kwargs)
            else:
                return f"Error: Unknown tool type '{tool.type}' for tool '{tool_name}'."

    def function_handler(self, function_def, **kwargs):
        # Dynamically import the function from the tools directory
        try:
            module = __import__(f"bacon.worker.tools.{function_def.name}", fromlist=[function_def.name])
            func = getattr(module, function_def.name)

            # For now, we will not do parameter validation.
            # This can be added back later if needed.

            return func(**kwargs)
        except ImportError:
            return f"Error: Could not import module for tool '{function_def.name}'."
        except AttributeError:
            return f"Error: Could not find function for tool '{function_def.name}'."
        except Exception as e:
            return f"An unexpected error occurred: {e}"

