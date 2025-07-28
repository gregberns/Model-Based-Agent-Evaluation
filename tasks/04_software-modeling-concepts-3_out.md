# The Virtual Plugin: A Blueprint for Agent-Driven Development (v3)

This document expands on our Virtual Plugin concept, clarifying its implementation, how it's used to test agent behavior, and how it fits into the broader project structure.

## 1. Schema Validation with Pydantic

To ensure all `plugin-profile.yaml` files are valid and to provide a reliable data model for our automation scripts, we will define a formal schema using **Pydantic**. This gives us a single source of truth for the model's structure.

A Python script (`framework/schema.py`) will contain the Pydantic models, which can then be used to parse, validate, and even generate JSON Schemas for the YAML files.

**Example: `framework/schema.py`**
```python
from pydantic import BaseModel, Field
from typing import List, Dict, Any

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
    expected_error: str = None # Optional field

class PluginProfile(BaseModel):
    name: str
    version: str # We'll use semantic versioning
    description: str
    mcp_profile: List[MCPTool]
    dependencies: List[str]
    configuration: List[Dict[str, str]]
    behavioral_profile: Dict[str, List[BehaviorScenario]]

# Usage:
# import yaml
# from framework.schema import PluginProfile
#
# with open("plugin-profile.yaml", "r") as f:
#     data = yaml.safe_load(f)
#     profile = PluginProfile(**data) # Pydantic validates on instantiation
#     print(f"Successfully validated {profile.name}")
```

## 2. The Virtual Plugin: A "Process Mock"

This is a critical clarification: a Virtual Plugin is **not** a partial implementation of the real plugin. It is a **Process Mock**. Its purpose is to test the *agent's ability to follow a playbook*, not to test the plugin's logic itself.

### 2.1. How it Works
The "source code" for a virtual plugin is a simple, generic script. This script's job is to read the `behavioral_profile` from its `plugin-profile.yaml` and simulate the defined outcomes. It does not contain any actual image processing, database logic, etc.

When an agent is tasked with "fixing a bug" in a virtual plugin, it does **not** add missing implementation. Instead, the agent's task is to **modify the `plugin-profile.yaml` to change the outcome of a scenario**.

**Example Workflow: Fixing a "Bug" in a Virtual Plugin**

1.  **Initial State:** The `behavioral_profile` defines a scenario that is expected to fail.
    ```yaml
    failure_scenarios:
      - description: "Resizing a zero-byte file causes an error."
        tool_call: "resize_image"
        inputs: { source_file: "test_data/empty.png" }
        expected_error: "InvalidFile"
        expected_log: "ERROR: File is empty or corrupted."
    ```
2.  **Agent's Task:** The playbook instructs the agent: "Fix the 'InvalidFile' bug for zero-byte files."
3.  **Agent's Action:** The agent edits the `plugin-profile.yaml`, moving the scenario from `failure_scenarios` to `success_scenarios` and defining the new, "fixed" behavior.
    ```yaml
    success_scenarios:
      - description: "Resizing a zero-byte file now returns a default placeholder image."
        tool_call: "resize_image"
        inputs: { source_file: "test_data/empty.png" }
        expected_log: "INFO: Empty file detected. Returning placeholder."
    ```
4.  **Verification:** The test harness re-runs the virtual plugin's test script. The script sees the updated profile and now "passes" for the `empty.png` input, confirming the "fix."

This approach ensures the agent is practicing the *process* of code modification, versioning, and testing, without needing a complex, real-world implementation.

## 3. Project Structure: Separating Virtual and Real Worlds

To manage virtual and real plugins, we will use a clear directory structure. The core framework can be configured to operate on either directory, allowing for safe testing and clean separation.

```
/poc-plugin-manager/
├── framework/
│   ├── __main__.py         # Main entrypoint for the manager
│   ├── schema.py           # Pydantic schemas
│   └── playbooks/          # Agent playbooks (TDD, bug fix, etc.)
│
├── plugins_virtual/        # Generated virtual plugins for testing the framework
│   ├── image-processor/
│   │   ├── plugin-profile.yaml
│   │   ├── src/main.py       # Generic virtual plugin runner
│   │   └── .history/         # Execution Traces (see section 5)
│   └── ...
│
└── plugins_real/           # Real, production-ready plugins
    ├── real-image-processor/
    │   ├── plugin-profile.yaml
    │   ├── src/main.py       # Actual implementation
    │   ├── CHANGE_LOG.md
    │   └── ...
    └── ...
```

A configuration file (`framework/config.yaml`) would specify the target directory: `plugin_directory: ./plugins_virtual`.

## 4. Playbooks, Versioning, and the `CHANGE_LOG.md`

### 4.1. Enhanced Playbook Steps
All playbooks that modify a plugin's code or behavior **must** include these final steps:

1.  **Increment Version:** Use a semantic versioning tool (e.g., `npm version patch` or a Python equivalent) to bump the version in `plugin-profile.yaml`.
2.  **Update Changelog:** Prepend the changes to a `CHANGE_LOG.md` file within the plugin's directory.

### 4.2. The `CHANGE_LOG.md`
This file is a human-readable history of changes for each plugin, maintained by the agents.

**`plugins_real/real-image-processor/CHANGE_LOG.md`**
```markdown
# Changelog

## [1.1.0] - 2025-07-26
### Added
- New `apply_watermark` tool.

## [1.0.1] - 2025-07-24
### Fixed
- Resolved issue where resizing a zero-byte file would cause an `InvalidFile` error.

## [1.0.0] - 2025-07-22
- Initial release.
```

## 5. Verifying Agent Actions: The "Execution Trace"

This is the key to testing our system. How do we assert that an agent *correctly followed the playbook*? We introduce the **Execution Trace**.

When an agent operates on a plugin, the framework will record key actions to a structured log file: `.history/execution_trace.jsonl`.

**Actions to be logged:**
*   `command_run`: The command, its exit code, stdout, and stderr.
*   `file_write`: The path of the file that was written to.
*   `version_change`: The old and new version numbers.

### 5.1. How it Works
A test harness, separate from the agent, can then parse this `execution_trace.jsonl` to verify the agent's behavior against the playbook's requirements.

**Example: Asserting the TDD Playbook**

A test for the TDD playbook would assert the following from the trace file:

1.  A `command_run` event exists for `pytest` where `exit_code != 0`.
2.  A `file_write` event exists for a path inside `src/`.
3.  A subsequent `command_run` event exists for `pytest` where `exit_code == 0`.
4.  A `version_change` event exists.
5.  A `file_write` event exists for `CHANGE_LOG.md`.

This provides a powerful, deterministic way to test that our agents are behaving as expected, making the entire system more robust and reliable. It tests the *process*, which is exactly what the Virtual Plugin is designed to mock.
