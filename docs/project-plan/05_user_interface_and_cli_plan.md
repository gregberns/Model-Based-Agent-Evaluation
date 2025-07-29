# 05 - User Interface and CLI Plan (Refined)

This document specifies the primary user interface for interacting with the plugin management framework.

## 1. Development Priority: Library First

The primary goal is to build a robust, composable **Python library**. The development of a user-facing CLI or `Makefile` is a **secondary priority** and will only be undertaken after the core library components (Orchestrator, Virtual Plugin Factory, Evaluation Harness) are implemented and well-tested.

## 2. Future CLI and `Makefile`

When the time comes to build a user interface, the plan outlined previously remains a sound approach.

### 2.1. Primary Interface: `Makefile`
A `Makefile` will provide a simple, self-documenting set of commands for the most common operations, wrapping the more complex Python CLI.

### 2.2. Core CLI: `packages/framework/__main__.py`
The `Makefile` will call the main entrypoint of our Python application. This CLI will be built using `argparse` and will be action-based, allowing the user to trigger different parts of the Orchestrator's functionality (e.g., `generate`, `run`).

## 3. Human-in-the-Loop (HITL) Interaction

The concept of HITL is important, but its implementation is **deferred**. The initial focus will be on fully-automated workflows that can be verified by the Evaluation Harness. Once the core automated system is proven to be reliable, HITL checkpoints can be added to the Orchestrator's workflow for sensitive operations in the `real` environment.

- **Mechanism:** Interactive console prompts.
- **Use Case:** Confirming destructive or significant changes, such as applying a generated patch to a real plugin's source code.
- **Automation Bypass:** A `--yes` flag will be included in the future CLI to allow for fully unattended execution in CI/CD pipelines.