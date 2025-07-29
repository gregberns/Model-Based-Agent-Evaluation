# 01 - Plugin Model and Structure: Technical Specification

This document provides the detailed technical specification for implementing the Plugin Model and its associated components.

## 1. Architecture and Design

The Plugin Model is centered around a `PluginProfile` data structure, which is validated by a Pydantic schema. This ensures that all interactions with the `plugin-profile.yaml` are type-safe and consistent. The logic for loading and validating profiles will be encapsulated in a dedicated `ProfileLoader` class to ensure reusability.

## 2. File and Class Structure

The implementation will be located within the `packages/framework` directory.

```
/packages/framework/
├── __init__.py
├── schema.py           # Pydantic models for the plugin profile.
├── profile_loader.py   # Class to load and validate profiles.
└── tests/
    ├── test_schema.py      # Unit tests for the Pydantic models.
    └── test_profile_loader.py # Unit tests for the loader.
```

### 2.1. `schema.py` - Pydantic Models

This file will contain the Pydantic class definitions that map directly to the `plugin-profile.yaml` structure.

```python
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
```

### 2.2. `profile_loader.py` - ProfileLoader Class

This class will handle the logic of finding, reading, parsing, and validating a `plugin-profile.yaml` file.

```python
# packages/framework/profile_loader.py

import yaml
from pathlib import Path
from .schema import PluginProfile

class ProfileLoader:
    """Loads and validates a plugin-profile.yaml file."""

    def load(self, plugin_directory: Path) -> PluginProfile:
        """
        Finds and loads the plugin profile from a given directory.

        Args:
            plugin_directory: The root directory of the plugin.

        Returns:
            A validated PluginProfile object.

        Raises:
            FileNotFoundError: If plugin-profile.yaml is not found.
            ValidationError: If the profile is invalid.
        """
        profile_path = plugin_directory / "plugin-profile.yaml"
        if not profile_path.is_file():
            raise FileNotFoundError(f"plugin-profile.yaml not found in {plugin_directory}")

        with open(profile_path, 'r') as f:
            data = yaml.safe_load(f)
            # Pydantic performs validation on instantiation
            profile = PluginProfile(**data)
            return profile
```

## 3. Implementation Order

Development will follow a TDD approach.

1.  **Implement `schema.py`:**
    -   Create the Pydantic models as defined above.
    -   Write `tests/test_schema.py` to validate the models. Tests should include:
        -   A valid, complete YAML example that parses successfully.
        -   An invalid example that raises a `ValidationError` (e.g., missing a required field).
        -   A test for the semantic versioning validator.
2.  **Implement `profile_loader.py`:**
    -   Create the `ProfileLoader` class.
    -   Write `tests/test_profile_loader.py`. Tests should include:
        -   Mocking a directory with a valid `plugin-profile.yaml` and asserting it loads correctly.
        -   Asserting that a `FileNotFoundError` is raised for a directory without the profile.
        -   Asserting that a `ValidationError` is propagated for a directory with an invalid profile.

## 4. Best Practices Applied

-   **Library First:** The `ProfileLoader` is a reusable class, and the `schema.py` is a reusable data model definition.
-   **Solid Abstractions:** The complexity of file reading, parsing, and validation is hidden behind a simple `load()` method.
-   **Testability:** Both components are pure Python and easily testable with `pytest` without complex mocks. The file system can be mocked using `pyfakefs` or by creating temporary files.
-   **DRY Principle:** The schema is defined in one place (`schema.py`) and is the single source of truth for the profile structure.
