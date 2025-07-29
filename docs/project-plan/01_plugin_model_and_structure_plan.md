# 01 - Plugin Model and Structure Plan

This document specifies the formal model and physical structure for all plugins managed by the system.

## 1. Core Component: `plugin-profile.yaml`

The `plugin-profile.yaml` is the single source of truth for a plugin. It is a machine-readable and human-editable file that defines the plugin's metadata, interface, configuration, and behavior.

### 1.1. Schema Definition
A formal schema for this file will be defined using **Pydantic** and located in `packages/framework/schema.py`. This will be used by the Orchestrator to validate any plugin it interacts with.

### 1.2. Top-Level Fields
- **`name` (string, required):** The unique, human-readable name of the plugin (e.g., "Image-Processing-Service").
- **`version` (string, required):** The current version of the plugin, adhering to **Semantic Versioning 2.0.0**.
- **`description` (string, required):** A brief description of the plugin's purpose.
- **`mcp_profile` (list, required):** Defines the plugin's interface using MCP-compliant tool definitions.
- **`dependencies` (list, optional):** A list of software or library dependencies (e.g., "python:flask").
- **`configuration` (list, optional):** A list of required environment variables.
- **`behavioral_profile` (object, optional):** Used by the Virtual Plugin Factory to simulate behavior.

### 1.3. Interface Definition: `mcp_profile`
This section defines the "tool calls" the plugin exposes.
- Each entry is an object with `name`, `description`, `parameters`, and `output`.
- `parameters` is an object where keys are argument names and values define the `type` and `description`.

### 1.4. Behavioral Profile
This section is used exclusively for testing and virtual plugin generation.
- **`success_scenarios` (list):** Defines predictable success cases.
- **`failure_scenarios` (list):** Defines predictable failure cases.
- Each scenario includes a `description`, the `tool_call` to invoke, `inputs`, and the `expected_log` output.

## 2. Physical Directory Structure

Every plugin, whether virtual or real, will adhere to a standardized directory structure.

```
/my-plugin/
├── plugin-profile.yaml     # The core model definition.
├── CHANGE_LOG.md           # Human-readable history of changes.
├── src/                    # Source code for the plugin.
├── tests/                  # Test suite for the plugin.
└── .history/               # (Virtual Plugins Only) For the execution trace.
```

## 3. Tradeoffs and Decisions

- **YAML vs. JSON:** YAML was chosen for the profile for its human-readability and support for comments, which is crucial for documentation. The Pydantic schema provides the programmatic safety.
- **MCP for Interface:** Using an MCP-style tool definition for the interface makes the plugins AI-native from the start. It avoids the need for an agent to parse OpenAPI specs or other API definitions, simplifying interaction.
- **Separation of Model and Code:** The `plugin-profile.yaml` is separate from the source code. This allows the Orchestrator to understand a plugin's capabilities and metadata without needing to parse the code itself.
