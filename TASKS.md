# Project Implementation Task List

This document outlines the concrete tasks required to build the Plugin Manager framework. Tasks should be checked off as they are completed.

**Master Plan:** [`docs/project-plan/00_master_plan.md`](./docs/project-plan/00_master_plan.md)

---

## Phase 1: The Virtual Plugin and Evaluation Foundation

*Goal: Build the components necessary to create and test a single, isolated virtual plugin.*

### 1.1. Project Scaffolding
- [ ] Create the `packages/framework` directory.
- [ ] Create the `packages/framework/tests` directory for unit tests.
- [ ] Create the `/evaluations` directory for end-to-end playbook tests.
- [ ] Create the `/templates` directory for Jinja2 templates.
- [ ] Create the `/playbooks` directory.

### 1.2. Plugin Model Schema
**Plan:** [`docs/project-plan/01_plugin_model_and_structure_plan.md`](./docs/project-plan/01_plugin_model_and_structure_plan.md)
**Tech Spec:** [`docs/project-plan/01_plugin_model_and_structure_plan__tech.md`](./docs/project-plan/01_plugin_model_and_structure_plan__tech.md)
- [x] **Code:** Implement all Pydantic models (`PluginProfile`, `MCPTool`, etc.) in `packages/framework/schema.py`.
- [x] **Test:** Write unit tests in `packages/framework/tests/test_schema.py` to validate the Pydantic models.

### 1.3. Core Loaders
**Tech Spec:** [`docs/project-plan/03_agent_playbooks_plan__tech.md`](./docs/project-plan/03_agent_playbooks_plan__tech.md)
- [x] **Code:** Implement the `ProfileLoader` class in `packages/framework/loaders.py`.
- [x] **Test:** Write unit tests in `packages/framework/tests/test_loaders.py` for the `ProfileLoader`.
- [x] **Code:** Implement the `Playbook` data class and the `PlaybookLoader` class in `packages/framework/loaders.py`.
- [x] **Test:** Write unit tests in `packages/framework/tests/test_loaders.py` for the `PlaybookLoader`.

### 1.4. Virtual Plugin Factory
**Plan:** [`docs/project-plan/04_virtual_plugin_factory_and_evaluation_plan.md`](./docs/project-plan/04_virtual_plugin_factory_and_evaluation_plan.md)
**Tech Spec:** [`docs/project-plan/04_virtual_plugin_factory_and_evaluation_plan__tech.md`](./docs/project-plan/04_virtual_plugin_factory_and_evaluation_plan__tech.md)
- [x] **Code:** Create the `virtual_main.py.j2` and `virtual_test.py.j2` Jinja2 templates in the `/templates` directory.
- [x] **Code:** Implement the `PluginFactory` class in `packages/framework/factory.py`.
- [x] **Test:** Write unit tests in `packages/framework/tests/test_factory.py` to ensure the factory correctly generates a virtual plugin.

### 1.5. Initial Playbook Asset
**Plan:** [`docs/project-plan/03_agent_playbooks_plan.md`](./docs/project-plan/03_agent_playbooks_plan.md)
- [x] **Asset:** Create the initial `playbook_fix_bug.md` file in the `/playbooks` directory.

### 1.6. Evaluation Harness
**Plan:** [`docs/project-plan/04_virtual_plugin_factory_and_evaluation_plan.md`](./docs/project-plan/04_virtual_plugin_factory_and_evaluation_plan.md)
**Tech Spec:** [`docs/project-plan/04_virtual_plugin_factory_and_evaluation_plan__tech.md`](./docs/project-plan/04_virtual_plugin_factory_and_evaluation_plan__tech.md)
- [x] **Code:** Implement the `EvaluationHarness` class in `evaluations/harness.py`.
- [x] **Test:** Create the structure for the first evaluation test in `evaluations/test_playbook_fix_bug.py`. Mark to be skipped (`@pytest.mark.skip`) until Phase 2.

---

## Phase 2: The Orchestrator and Agent Integration

*Goal: Build the engine that connects the agent to the tools and playbooks, and run the first end-to-end evaluation.*

### 2.1. Event System & Tooling
**Plan:** [`docs/project-plan/02_orchestrator_framework_plan.md`](./docs/project-plan/02_orchestrator_framework_plan.md)
**Tech Spec:** [`docs/project-plan/02_orchestrator_framework_plan__tech.md`](./docs/project-plan/02_orchestrator_framework_plan__tech.md)
- [x] **Code:** Implement the `EventEmitter` class in `packages/framework/events.py`.
- [x] **Test:** Write unit tests for the `EventEmitter`.
- [x] **Code:** Implement the `wrap_tool` decorator in `packages/framework/tool_wrapper.py`.
- [x] **Test:** Write unit tests for `wrap_tool` to ensure it emits events correctly.

### 2.2. Prompt Construction
**Tech Spec:** [`docs/project-plan/03_agent_playbooks_plan__tech.md`](./docs/project-plan/03_agent_playbooks_plan__tech.md)
- [x] **Code:** Implement the `PromptConstructor` class in `packages/framework/prompt_constructor.py`.
- [x] **Test:** Write unit tests for the `PromptConstructor`.

### 2.3. Orchestrator Engine
**Plan:** [`docs/project-plan/02_orchestrator_framework_plan.md`](./docs/project-plan/02_orchestrator_framework_plan.md)
**Tech Spec:** [`docs/project-plan/02_orchestrator_framework_plan__tech.md`](./docs/project-plan/02_orchestrator_framework_plan__tech.md)
- [x] **Code:** Implement the `Orchestrator` class in `packages/framework/orchestrator.py`.
- [x] **Test:** Write unit tests for the `Orchestrator`, mocking the `GeminiAgent`.

### 2.4. Final Integration and End-to-End Evaluation
- [ ] **Integration:** Update the `GeminiAgent` to accept the wrapped toolset from the Orchestrator.
- [ ] **Evaluation:** Complete the `evaluations/test_playbook_fix_bug.py` test, running a full playbook execution on a virtual plugin and asserting against the captured events.
- [ ] **CI:** Ensure the evaluation test runs successfully in a CI environment.

---

## Phase 3: Real Plugin Environment and User Interface

*Goal: Enable the system to operate on real code and provide a user-friendly interface.*

### 3.1. Real Environment
- [ ] **Code:** Add the logic to the Orchestrator and CLI to handle the `/plugins_real` directory.
- [ ] **Asset:** Create the `/plugins_real` directory.

### 3.2. User Interface (Deferred)
**Plan:** [`docs/project-plan/05_user_interface_and_cli_plan.md`](./docs/project-plan/05_user_interface_and_cli_plan.md)
**Tech Spec:** [`docs/project-plan/05_user_interface_and_cli_plan__tech.md`](./docs/project-plan/05_user_interface_and_cli_plan__tech.md)
- [ ] **Code:** Implement the core CLI logic in `packages/framework/__main__.py`.
- [ ] **Test:** Write integration tests for the CLI.
- [ ] **Code:** Implement Human-in-the-Loop (HITL) confirmation prompts.
- [ ] **Code:** Create the `Makefile` in the project root.

### 3.3. Dogfooding
- [ ] **Task:** Use the completed system to execute a "create new plugin" playbook to generate the first real, production-ready plugin.