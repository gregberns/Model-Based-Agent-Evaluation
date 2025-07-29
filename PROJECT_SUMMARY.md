# Project Summary: Plugin Manager Framework

## 1. Vision & Core Problem

The project's goal is to build a scalable, agent-driven framework for managing and maintaining a large library of software plugins. The core problem is automating complex software engineering tasks (bug fixes, feature implementation) in a reliable, observable, and testable way.

## 2. Core Architecture

The system is composed of three main conceptual pieces:

1.  **The Orchestrator:** A deterministic Python library that manages the entire workflow. It is the "engine" of the system.
2.  **The Agent:** A Large Language Model (our `GeminiAgent`) that provides the reasoning and decision-making capabilities. It is controlled by the Orchestrator.
3.  **The Playbooks:** Version-controlled markdown files that define high-level, implementation-agnostic goals for the Agent (e.g., "Fix this bug using TDD").

The interaction model is an **"Observability Wrapper" pattern**. The Orchestrator provides our own custom-built, observable tools (like `edit_file`) to the Agent via the Gemini SDK's function-calling mechanism. The Agent has no direct access to the environment; it can only *request* that the Orchestrator use a tool. This makes every action the Agent takes explicit, safe, and loggable.

## 3. Key Technical Decisions

-   **Library First:** The primary output is a composable Python library, not a monolithic application. The CLI is a thin wrapper to be built later.
-   **Custom Tools:** We are using our own well-defined toolset (especially the `edit_file` tool) to ensure reliability and control, explicitly avoiding external, unstable toolkits.
-   **Event-Driven Logging:** The Orchestrator uses an event-emitter system. Tool wrappers emit events (`tool_requested`, `tool_completed`) which are captured by listeners for logging or evaluation. This decouples observability from the core logic.
-   **Pydantic for Schemas:** The `plugin-profile.yaml`, which is the source of truth for any plugin, is strictly validated by a Pydantic schema.

## 4. The Testing Strategy: Virtual Plugins

The cornerstone of our development and testing strategy is the **Virtual Plugin**.

-   **What it is:** A "Process Mock"—a simple, deterministic, simulated plugin that is auto-generated from a `plugin-profile.yaml`. Its code is a generic interpreter of the profile's `behavioral_profile` section.
-   **Its Purpose:** To test the Agent's ability to correctly follow a high-level Playbook. The Agent "fixes a bug" in a virtual plugin by editing its `plugin-profile.yaml` to change the simulated outcome.
-   **Verification:** An **Evaluation Harness** runs a playbook on a virtual plugin and captures the stream of events from the Orchestrator. It then asserts that the sequence of tool calls matches the steps defined in the playbook, providing a robust, automated way to validate the agent's reasoning process.

## 5. Current Status & Next Steps

The project is in the **planning complete** stage. The next step is to begin **Phase 1** of implementation, as detailed in `TASKS.md`. The immediate focus is on building the foundational components for the virtual plugin and evaluation system, following a TDD methodology.
