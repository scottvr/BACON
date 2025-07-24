
from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class ToolParameter(BaseModel):
    name: str
    type: Literal["string", "filepath", "integer", "boolean"]
    required: bool = True
    description: Optional[str] = None

class ToolConfig(BaseModel):
    api_key_env: Optional[str] = None
    base_url: Optional[str] = None
    command: Optional[List[str]] = None
    params: List[ToolParameter] = []

class ToolDefinition(BaseModel):
    name: str
    description: str
    type: Literal["api", "cli", "function"]
    handler: str
    requires_approval: bool = False
    config: ToolConfig

class ToolsConfig(BaseModel):
    tools: List[ToolDefinition]
