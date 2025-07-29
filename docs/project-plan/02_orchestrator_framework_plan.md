# 02 - Orchestrator Framework Plan (Refined)

This document specifies the architecture of the core framework, referred to as the Orchestrator.

## 1. Core Responsibility

The Orchestrator is a deterministic Python application responsible for managing the entire lifecycle of a plugin maintenance task. It is built as a **composable library** of reusable components. It acts as the intermediary between the high-level instructions in a Playbook and the reasoning capabilities of an AI Agent. Its primary function is to provide a safe, observable environment for the agent to operate in.

## 2. Architecture: The "Observability Wrapper" Pattern

The Orchestrator implements the "Observability Wrapper" pattern.
- It programmatically controls the `GeminiAgent` (defined in `packages/plugin_manager_agent`) via its Python interface.
- It provides the Agent with a set of approved **Tools** using the Gemini SDK's function calling mechanism.
- The Agent has **no direct access** to the filesystem or shell. It can only *request* that the Orchestrator execute a tool on its behalf.

This architecture is the key to safety and verifiability.

## 3. Key Components

The Orchestrator will be built from well-abstracted, reusable modules.

### 3.1. Composable Libraries
- **Profile Loader:** A module responsible for finding, loading, and validating a `plugin-profile.yaml` file using the Pydantic schema.
- **Playbook Loader:** A module for loading a `playbook.md` file.
- **Prompt Constructor:** A module that takes a profile, a playbook, and environment details to construct the final, contextualized prompt for the Agent.

### 3.2. Orchestrator Engine (`packages/framework/orchestrator.py`)
- Contains the main execution loop that integrates the composable libraries.
- **Responsibilities:**
    1.  Use the loaders to get the plugin profile and playbook.
    2.  Use the prompt constructor to build the initial prompt.
    3.  Instantiate and initiate the chat session with the `GeminiAgent`.
    4.  Enter the manual function-calling loop:
        - Receive a tool call request from the Agent.
        - **Emit a `tool_requested` event.**
        - Execute the corresponding tool function via the Tool Wrapper.
        - **Emit a `tool_completed` or `tool_failed` event with the result.**
        - Send the result back to the Agent.
    5.  Continue looping until the Agent responds with a final text summary.

### 3.3. Toolset and Event System
- **Toolset:** The tools provided to the agent are our own, defined in `packages/plugin_manager_agent/tools`. This includes the robust `edit_file` tool. We will **not** use external toolkits like Composio or SWE-Kit.
- **Event Emitter/Handler:** The framework will implement a simple event system. The tool wrappers will be the primary emitters.
- **Tool Wrappers:** Before being passed to the agent, each tool function will be wrapped. When the agent calls a tool, the wrapper will:
    1. Emit a `tool_requested` event with the function name and arguments.
    2. Execute the actual tool function.
    3. Emit a `tool_completed` or `tool_failed` event with the result.
- **Event Listeners (Logging):** A logger module will listen for these events and write them to the `execution_trace.jsonl` file. This decouples the logging from the execution.

## 4. Tradeoffs and Decisions

- **Python SDK vs. Headless CLI:** Using our own `GeminiAgent` class, which is a wrapper around the official Python SDK, provides the robust control needed for the function-calling loop. This is superior to managing a separate CLI process.
- **Our Tools vs. External Tools:** We are explicitly using our own well-defined toolset. This avoids the brittleness and dependency issues of external, rapidly changing libraries and gives us full control over the agent's capabilities. The `edit_file` tool we designed is specifically suited for our needs.
- **Manual Function Calling:** We will continue to use manual function calling in the `GeminiAgent`. This is the essential mechanism that allows the Orchestrator to intercept, log, and safely execute the agent's requested actions.