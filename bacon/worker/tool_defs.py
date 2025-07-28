from pydantic import BaseModel, Field
from typing import List, Optional, Union, Literal

class FunctionParameter(BaseModel):
    type: str
    description: Optional[str] = None
    enum: Optional[List[str]] = None

class FunctionDefinition(BaseModel):
    name: str
    description: str
    parameters: dict[str, FunctionParameter]

class ToolDefinition(BaseModel):
    type: Literal["function"]
    function: FunctionDefinition

class ToolsConfig(BaseModel):
    tools: List[ToolDefinition]
