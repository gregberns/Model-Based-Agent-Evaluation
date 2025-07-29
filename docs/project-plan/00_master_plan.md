# 00 - Master Project Plan (Refined)

This document provides the high-level overview of the Plugin Manager project, defines the core components, and specifies the refined order of implementation.

## 1. Project Vision

To create a scalable, agent-driven system for managing a large library of software plugins. The framework will use an AI agent to automate complex software maintenance tasks (e.g., bug fixes, feature development) by executing standardized, version-controlled **Playbooks**. The entire system is designed to be highly observable and testable through the use of **Virtual Plugins** and **Execution Traces**.

## 2. Core Components

The project is broken down into five key components, each with its own detailed specification document:

1.  **[Plugin Model and Structure](./01_plugin_model_and_structure_plan.md):** Defines the `plugin-profile.yaml` which is the source of truth for a plugin's metadata, interface, and behavior. It also defines the standardized directory structure for all plugins.
2.  **[Orchestrator Framework](./02_orchestrator_framework_plan.md):** The core Python application that manages and executes playbooks. It uses an "Observability Wrapper" pattern to safely control an AI agent and log all of its actions.
3.  **[Agent Playbooks](./03_agent_playbooks_plan.md):** The high-level, version-controlled instructions that guide the AI agent. A single, canonical set of playbooks is used for both virtual and real plugins.
4.  **[Virtual Plugin Factory and Testing](./04_virtual_plugin_factory_and_testing_plan.md):** The system for generating "Process Mock" plugins from a profile. These virtual plugins are used in an evaluation harness to verify the agent's ability to follow playbooks by analyzing a logged "Execution Trace".
5.  **[User Interface and CLI](./05_user_interface_and_cli_plan.md):** The primary interface for the system, which will be built *after* the core library components are complete.

## 3. Development and Implementation Order

The project will be implemented in small, testable steps, prioritizing the Virtual Plugin system to enable a Test-Driven Development (TDD) workflow for the entire framework.

### Phase 1: The Virtual Plugin and Evaluation Foundation

*Goal: Build the components necessary to create and test a single, isolated virtual plugin.*

1.  **Plugin Model Schema:** Implement the Pydantic models for the `plugin-profile.yaml` in `packages/framework/schema.py`.
2.  **Virtual Plugin Factory:** Implement the script to generate a complete virtual plugin from a `plugin-profile.yaml` located within the plugin's own directory.
3.  **Evaluation Harness:** Create the initial evaluation harness. This will be a test suite (e.g., in `evaluations/`) that can run a playbook on a virtual plugin and assert against the resulting execution trace.
4.  **Develop Initial Playbook:** Write the first canonical playbook (e.g., `playbook_fix_bug.md`) to be used for testing.

### Phase 2: The Orchestrator and Agent Integration

*Goal: Build the engine that connects the agent to the tools and playbooks.*

1.  **Composable Orchestrator Components:** Build the core, reusable components of the Orchestrator (profile loader, playbook loader, prompt constructor) as well-abstracted modules.
2.  **Event System and Tool Wrappers:** Implement the event-emitting system. Wrap the tools from `packages/plugin_manager_agent/tools` in observable wrappers that emit events for logging and tracing.
3.  **Integrate Gemini Agent:** Wire the Orchestrator to the `GeminiAgent`, implementing the manual function-calling loop to intercept and dispatch tool calls through the event system.
4.  **End-to-End Evaluation:** Use the Evaluation Harness built in Phase 1 to run the first end-to-end test: the Orchestrator executes a playbook with the live Agent on a virtual plugin, and the test asserts the correctness of the generated execution trace.

### Phase 3: Real Plugin Environment and CLI

*Goal: Enable the system to operate on real code and provide a user interface.*

1.  **Implement Real Environment Logic:** Add the logic to the Orchestrator to operate on the `/plugins_real` directory.
2.  **Build Core CLI:** Once the core libraries are stable and well-tested, build the main CLI entrypoint to expose the Orchestrator's functionality.
3.  **Human-in-the-Loop:** Implement the confirmation prompts for critical actions in the `real` environment as part of the CLI.
4.  **Create First Real Plugin:** Use the system itself to execute a "create new plugin" playbook to generate the first real, production-ready plugin.