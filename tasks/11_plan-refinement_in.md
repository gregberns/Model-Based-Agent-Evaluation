Below are a whole bunch of changes that need to be made to the plan generated in `docs/project-plan`.

The documents that were used to build that plan had some incorrect assumptions and failed paths. 

It is VERY IMPORTANT that you make sure to remove some of the ideas I mention below - otherwise subsequent steps/Agents will fail because the followed incorrect directions, invalid ideas, or use tech that doesn't exist.

## Master Plan

The approach of the Master Plan assumes we know what the Orchestrator is going to look like and how its going to call everything else.

The Virtual Plugin system is core to this framework. I'd like to start by building out some of the component pieces. I think that will lead to a system thats more testable/verifiable/evaluatable.

A large part of this project is to build out the Virtual Plugin system. Once that is built we can start building the orchestrator and immediately start running it to see if its working as we'd expect.

If we have a single Virtual Plugin, we can have the agent operate on it, then have the orchestrator do a couple things, then wrap the tooling so we can track or mock things - whatever that looks like.

Small steps will allow us to validate what we're building as we go.

When writing code, we should be following a TDD workflow.

## Master Plan - Tool Wrappers

This is not correct.

```
3.  **Tool Wrappers & Logging:** Implement the "Observability Wrapper" for the core Composio SWE-Kit tools (`ReadFile`, `PatchFile`, `ExecuteShellCommand`). Implement the event logger to produce the `execution_trace.jsonl`.
```

Neither `Composio` or `SWE-Kit` will be used AT ALL! Any where these are referenced, they should be removed and corrected.

We'll be using the agent defined here `packages/plugin_manager_agent/gemini_agent.py`, and there are several tools defined in `packages/plugin_manager_agent/tools` including `edit_file`, `execute_shell_command`, `list_files` and `read_file`.

We'll need to figure out how to wrap the tools - but now that we control them, we should be able to do that.


## Orchestrator

This block is not entirely correct. 

```
## 2. Architecture: The "Observability Wrapper" Pattern

The Orchestrator implements the "Observability Wrapper" pattern.
- It programmatically controls the Agent (Gemini) via the official Python SDK.
- It provides the Agent with a set of approved **Tools** (e.g., `read_file`, `patch_file`) using the SDK's function calling mechanism.
- The Agent has **no direct access** to the filesystem or shell. It can only *request* that the Orchestrator execute a tool on its behalf.
```

The Orchestrator will need to pass a set of tools to the Agent it can use to perform actions. This will allow tracking everything that occurs when Virtual Plugins are called.


### Orchestrator - Details

The Orchestrtator should be built as a series of composible libraries, integrated together and executable via command line arguments that the main orchestrator module will perform.

### 3.2. Orchestrator Engine

Each of the components we're building needs to be built with best practices - they need to be well abstracted, in their  own resuable files/modules/classes.

For example, each of these components will need to be well structured, independent/reusable - following the DRY principle.
```
    1.  Load the specified plugin's `plugin-profile.yaml`.
    2.  Load the specified `playbook.md`.
    3.  Construct the initial, contextualized prompt for the Agent.
```


In this section, this is where we'll need to build great re-usable wrappers that can wrap the tools for logging/tracing and to intercept the calls where needed.

```
    5.  Enter a loop:
        - Receive a tool call request from the Agent.
        - Log the request to the Execution Trace.
        - Execute the corresponding tool function.
        - Log the result of the tool execution.
        - Send the result back to the Agent.
```

This section needs to be updated - its almost totally wrong. Details were provided above.

```
### 3.3. Toolset (`packages/framework/tools/`)
- The tools provided to the agent will be based on the **Composio SWE-Kit**.
- We will not re-implement complex tools. Instead, we will import them from the `composio-python` library.
- Each tool will be wrapped in a simple function that adds our logging hooks before and after calling the real tool. This gives us our observability layer.
- The primary file modification tool will be `PatchFile`, which applies standard `diff` patches.
```

This should really be modeled as an event emiting/handling system. It then can be hooked into for logging, tracing, and more.

```
### 3.4. Event Logger (`packages/framework/logger.py`)
- A simple logger responsible for writing structured events (e.g., `tool_requested`, `tool_completed`) to the plugin's `.history/execution_trace.jsonl` file.
```


# 03 - Agent Playbooks Plan

I think this document looks good.

# 04 - Virtual Plugin Factory and Testing Plan

Like I said before, I think this is one of the first things we should probably work on. If it makes sense to build out the Agent Playbooks first - thats fine, they're pretty simple.

### Process

I don't think there should be a `/plugin_profiles` directory. For the real plugins the yaml file needs to be stored in the plugin. I think we should also just put the yaml file in `/plugins_virtual/my-plugin/`.

```
### 2.1. Process
1.  **Input:** Takes the path to a master `plugin-profile.yaml` from the `/plugin_profiles` directory.
2.  **Scaffolding:** Creates a new directory in `/plugins_virtual/my-plugin/`.

```

### Test Harness

Putting the this module in `packages/framework/tests` makes it seem like the folder is for unit testing - but this is really more like evaluation. 

```
### 3.1. Test Harness
A separate test harness (e.g., `pytest packages/framework/tests/test_playbooks.py`) will be responsible for verifying the correctness of a playbook execution.
```

It'll be good to be able to write to a file, but as part of the test, all that data probably can be captured and stored in memory - through the event system mentioned above.

```
2.  After the Orchestrator finishes, the test harness will parse the resulting `execution_trace.jsonl`.
```

# 05 - User Interface and CLI Plan

As of now, we need to focus on getting all component parts build out. Once we have them structured as a series of libraries we can compose together, then we'll be able to do things like expose functionality through a CLI and maybe even a REST server.

Just don't go and implement anything regarding this until we have the core system built out.

```
## 3. Human-in-the-Loop (HITL) Interaction

While the system is designed for automation, certain critical steps will require human confirmation. The primary mechanism for this will be interactive prompts in the console.

- **Where to Prompt:** The Orchestrator will prompt for confirmation at key decision points, such as before an agent-generated `diff` is applied to a real plugin's source code.
- **`--yes` Flag:** The `run-playbook` action will include a `--yes` flag to bypass these confirmation prompts, allowing for fully unattended execution in trusted CI/CD environments.
```
