# packages/framework/schema.py

from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Any, Optional

class MCPParameter(BaseModel):
    type: str
    description: str

class MCPTool(BaseModel):
    name: str
    description: str
    parameters: Dict[str, MCPParameter]
    output: Dict[str, Any]

class BehaviorScenario(BaseModel):
    description: str
    tool_call: str
    inputs: Dict[str, Any]
    expected_log: str
    expected_error: Optional[str] = None

class BehavioralProfile(BaseModel):
    success_scenarios: List[BehaviorScenario] = []
    failure_scenarios: List[BehaviorScenario] = []

class ConfigurationItem(BaseModel):
    name: str
    description: str
    default: str

class PluginProfile(BaseModel):
    name: str
    version: str
    description: str
    mcp_profile: List[MCPTool]
    dependencies: Optional[List[str]] = []
    configuration: Optional[List[ConfigurationItem]] = []
    behavioral_profile: Optional[BehavioralProfile] = None

    @field_validator('version')
    def validate_semantic_version(cls, v):
        # Basic semantic versioning check (e.g., "1.2.3")
        parts = v.split('.')
        if len(parts) != 3 or not all(part.isdigit() for part in parts):
            raise ValueError('Version must be in semantic versioning format (e.g., "1.0.0")')
        return v
