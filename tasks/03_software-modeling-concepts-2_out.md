# The Virtual Plugin: A Blueprint for Agent-Driven Development

This document provides a detailed blueprint for the **"Virtual Plugin"** concept. It serves as a formal model for defining, generating, and managing software components at scale using an agent-driven methodology.

## 1. The Core Model: `plugin-profile.yaml`

The single source of truth for any plugin is its `plugin-profile.yaml`. This file is a declarative, human-readable, and version-controlled definition that provides all the necessary information for an agent to understand, build, test, and maintain the plugin.

### 1.1. Top-Level Structure

```yaml
# The formal model definition for a virtual plugin
name: "Image-Processing-Service"
version: "1.0.0"
description: "A microservice that resizes and applies watermarks to images."

# The MCP-compliant interface for the plugin
mcp_profile:
  # ... (see section 1.2)

# Software and library dependencies
dependencies:
  - "python:flask"
  - "library:pillow"

# Environment variable configuration
configuration:
  - name: "CACHE_SIZE_MB"
    description: "The maximum size of the image cache."
    default: "1024"
  - name: "WATERMARK_TEXT"
    description: "The text to apply as a watermark."
    default: "Confidential"

# Behavioral model for simulation and testing
behavioral_profile:
  # ... (see section 1.3)
```

### 1.2. The MCP Profile: Defining the Plugin's Interface

Instead of a traditional REST API, each plugin exposes its functionality through a set of **tool calls** that adhere to the Model Context Protocol (MCP) specification. This provides a standardized, AI-native interface for all plugins in the ecosystem.

The `mcp_profile` is an array of tool definitions.

```yaml
mcp_profile:
  - name: "resize_image"
    description: "Resizes an image to the specified dimensions."
    parameters:
      source_file: { type: "string", description: "Path to the source image file." }
      width: { type: "integer", description: "The target width in pixels." }
      height: { type: "integer", description: "The target height in pixels." }
    output:
      type: "string"
      description: "Path to the resized image file."

  - name: "apply_watermark"
    description: "Applies a text watermark to an image."
    parameters:
      source_file: { type: "string", description: "Path to the source image file." }
      text: { type: "string", description: "The watermark text to apply." }
    output:
      type: "string"
      description: "Path to the watermarked image file."
```

### 1.3. The Behavioral Profile: Simulating Reality

The `behavioral_profile` is crucial for generating realistic mock code and synthetic data. It defines specific success and failure scenarios that the generated plugin must simulate.

```yaml
behavioral_profile:
  # Scenarios that should succeed and produce predictable output
  success_scenarios:
    - description: "A 10MB PNG file is successfully resized to 800x600."
      tool_call: "resize_image"
      inputs: { source_file: "test_data/large.png", width: 800, height: 600 }
      expected_log: "INFO: Image resized successfully to output/large_resized.png"

    - description: "A JPG file has the default watermark applied."
      tool_call: "apply_watermark"
      inputs: { source_file: "test_data/photo.jpg", text: "Confidential" }
      expected_log: "INFO: Watermark applied successfully to output/photo_watermarked.jpg"

  # Scenarios that should fail in a predictable way
  failure_scenarios:
    - description: "An unsupported file type (TIFF) is submitted."
      tool_call: "resize_image"
      inputs: { source_file: "test_data/unsupported.tiff", width: 800, height: 600 }
      expected_error: "UnsupportedFileType"
      expected_log: "ERROR: Unsupported file type 'tiff'. Cannot process."

    - description: "The input file is corrupted or missing."
      tool_call: "apply_watermark"
      inputs: { source_file: "test_data/nonexistent.jpg", text: "Error" }
      expected_error: "FileNotFound"
      expected_log: "ERROR: Input file not found at path: test_data/nonexistent.jpg"
```

## 2. Agent Playbooks: Standardized Task Execution

An **Agent Playbook** is a set of version-controlled, templated instructions that guide a software agent to perform a specific, complex task (e.g., "Create a new feature," "Debug a production error").

Playbooks are stored in a central `/playbooks` directory.

`/playbooks/
├── TDD_workflow/
│   ├── playbook.md
│   └── prompt_templates/
│       ├── 01_write_failing_test.txt
│       ├── 02_implement_feature.txt
│       └── 03_refactor_code.txt
└── ... (other playbooks)`

### Example: TDD Workflow Playbook

The `playbook.md` for a TDD workflow would orchestrate the entire process:

**`playbooks/TDD_workflow/playbook.md`**
```markdown
# Playbook: Test-Driven Development Workflow

**Objective:** To implement a new feature in the plugin defined by `plugin-profile.yaml` using a strict TDD methodology.

**Agent Persona:** You are a senior software engineer specializing in Test-Driven Development. You write clean, minimal code and always start with a failing test.

**Steps:**

1.  **Understand the Goal:** Read the provided feature description and the `plugin-profile.yaml`.
2.  **Write a Failing Test (Step 1):**
    *   Use the `01_write_failing_test.txt` prompt template.
    *   Identify the relevant tool call from the `mcp_profile`.
    *   Write a new test case that calls this tool and asserts the expected outcome.
    *   **Execute the test suite and confirm that the new test fails.**
3.  **Implement the Feature (Step 2):**
    *   Use the `02_implement_feature.txt` prompt template.
    *   Write the minimum amount of code required to make the failing test pass.
    *   **Execute the test suite and confirm that all tests now pass.**
4.  **Refactor (Step 3):**
    *   Use the `03_refactor_code.txt` prompt template.
    *   Review the newly added code and refactor for clarity, efficiency, and adherence to coding standards.
    *   **Execute the test suite one last time to ensure no regressions were introduced.**
```

## 3. The Plugin Factory: Generating Virtual Plugins

The **Plugin Factory** is an automated script (`create_plugin.sh`) that instantiates a Virtual Plugin from its `plugin-profile.yaml`.

**Execution:**
```bash
./scripts/create_plugin.sh --profile ./plugin_profiles/image_processor.yaml --output ./generated_plugins/
```

**Process:**

1.  **Parse Profile:** Reads and validates the `plugin-profile.yaml`.
2.  **Scaffold Directory:** Creates the plugin's root directory and subdirectories (`src`, `tests`, `logs`).
3.  **Generate Mock Server (LLM Call):**
    *   Constructs a detailed prompt containing the `mcp_profile` and `behavioral_profile`.
    *   Asks an LLM to generate a mock server (e.g., `src/main.py` in Flask) that:
        *   Implements functions for each tool in the `mcp_profile`.
        *   Simulates the logic from the `behavioral_profile`, including success and failure cases.
        *   Writes the `expected_log` messages to stdout/stderr.
4.  **Generate Synthetic Logs:**
    *   Executes the generated mock server for each scenario in the `behavioral_profile`.
    *   Pipes the output to `logs/success.log` and `logs/error.log`.
5.  **Generate Documentation:** Creates a `README.md` populated with information from the profile.

### Generated `README.md` Example

```markdown
# Image-Processing-Service

**Version:** 1.0.0

A microservice that resizes and applies watermarks to images.

## Interface (MCP Tools)

### `resize_image`
Resizes an image to the specified dimensions.
- **Parameters:**
  - `source_file` (string): Path to the source image file.
  - `width` (integer): The target width in pixels.
  - `height` (integer): The target height in pixels.
- **Output:** (string) Path to the resized image file.

### `apply_watermark`
Applies a text watermark to an image.
- **Parameters:**
  - `source_file` (string): Path to the source image file.
  - `text` (string): The watermark text to apply.
- **Output:** (string) Path to the watermarked image file.

## Configuration

- `CACHE_SIZE_MB`: The maximum size of the image cache. (Default: 1024)
- `WATERMARK_TEXT`: The text to apply as a watermark. (Default: "Confidential")
```

This structured, model-driven approach provides a powerful and scalable foundation for developing, testing, and managing a large ecosystem of plugins with AI agents.
