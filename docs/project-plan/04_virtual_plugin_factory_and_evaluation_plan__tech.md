# 04 - Virtual Plugin Factory and Evaluation: Technical Specification

This document provides the detailed technical specification for the Virtual Plugin Factory and the Evaluation Harness.

## 1. Architecture and Design

This system has two main parts: the `PluginFactory`, which generates the test assets, and the `EvaluationHarness`, which runs the tests and makes assertions.

-   **`PluginFactory`:** A class responsible for creating a complete, self-contained virtual plugin directory from a `plugin-profile.yaml`.
-   **`EvaluationHarness`:** A class that uses the `Orchestrator` to run a playbook on a virtual plugin and captures the resulting events to verify the agent's performance. It will be built on top of `pytest`.

## 2. File and Class Structure

```
/packages/framework/
├── __init__.py
├── factory.py          # The PluginFactory class.
└── tests/
    └── test_factory.py

/evaluations/
├── __init__.py
├── harness.py          # The EvaluationHarness class.
└── test_playbook_fix_bug.py # An example evaluation test.

/templates/               # Templates for generated files
├── virtual_main.py.j2
└── virtual_test.py.j2
```

### 2.1. `factory.py` - PluginFactory Class

This class will use templates (e.g., Jinja2) to generate the mock server and test files.

```python
# packages/framework/factory.py

from pathlib import Path
import shutil
from jinja2 import Environment, FileSystemLoader
from .schema import PluginProfile

class PluginFactory:
    """Generates a virtual plugin from a profile."""

    def __init__(self, template_dir: Path):
        self.template_env = Environment(loader=FileSystemLoader(template_dir))

    def create(self, profile: PluginProfile, output_dir: Path) -> Path:
        """
        Creates the virtual plugin directory structure and files.

        Args:
            profile: The plugin profile object.
            output_dir: The root directory where the plugin will be created.

        Returns:
            The path to the newly created plugin directory.
        """
        plugin_path = output_dir / profile.name
        if plugin_path.exists():
            shutil.rmtree(plugin_path) # Ensure a clean slate
        
        # Create directories
        src_path = plugin_path / "src"
        tests_path = plugin_path / "tests"
        history_path = plugin_path / ".history"
        src_path.mkdir(parents=True)
        tests_path.mkdir()
        history_path.mkdir()

        # Write the profile back to the new directory
        shutil.copy(profile_path, plugin_path / "plugin-profile.yaml")

        # Generate mock server from template
        main_template = self.template_env.get_template("virtual_main.py.j2")
        main_content = main_template.render(profile=profile)
        (src_path / "main.py").write_text(main_content)

        # Generate mock tests from template
        test_template = self.template_env.get_template("virtual_test.py.j2")
        test_content = test_template.render(profile=profile)
        (tests_path / "test_virtual.py").write_text(test_content)
        
        return plugin_path
```

### 2.2. `harness.py` - EvaluationHarness Class

This class provides a clean interface for running evaluations.

```python
# evaluations/harness.py

from typing import List, Dict, Any
from packages.framework.orchestrator import Orchestrator
from packages.framework.events import event_emitter

class EvaluationHarness:
    """Runs a playbook and captures events for assertion."""

    def __init__(self, orchestrator: Orchestrator):
        self.orchestrator = orchestrator
        self.captured_events: List[Dict[str, Any]] = []

    def _event_listener(self, data: Dict[str, Any]):
        """Appends captured events to the internal list."""
        self.captured_events.append(data)

    def run_and_capture(self, *args, **kwargs) -> List[Dict[str, Any]]:
        """
        Runs the orchestrator and captures all emitted events.
        """
        self.captured_events = [] # Reset
        event_emitter.on("tool_requested", self._event_listener)
        event_emitter.on("tool_completed", self._event_listener)
        event_emitter.on("tool_failed", self._event_listener)

        self.orchestrator.run(*args, **kwargs)

        return self.captured_events
```

### 2.3. `test_playbook_fix_bug.py` - Example Evaluation

This is a `pytest` test file showing how the harness is used.

```python
# evaluations/test_playbook_fix_bug.py

from .harness import EvaluationHarness
# ... other necessary imports for factory, orchestrator, etc.

def test_fix_bug_playbook_on_virtual_plugin():
    # 1. Setup
    # (Instantiate factory, orchestrator, agent mocks, etc.)
    harness = EvaluationHarness(orchestrator)
    
    # Create a virtual plugin for this test run
    # ...

    # 2. Execute
    events = harness.run_and_capture(
        playbook_path="playbooks/playbook_fix_bug.md",
        plugin_path=virtual_plugin_path,
        env="virtual",
        bug_description="A test bug."
    )

    # 3. Assert
    # Find the relevant events in the captured list
    pytest_runs = [e for e in events if e.get("args", {}).get("command") == "pytest"]
    edit_file_calls = [e for e in events if e["name"] == "edit_file"]

    assert len(pytest_runs) >= 2
    assert pytest_runs[0]["result"]["exit_code"] != 0
    assert pytest_runs[1]["result"]["exit_code"] == 0
    
    assert any("plugin-profile.yaml" in call["args"]["file_path"] for call in edit_file_calls)
    assert any("CHANGE_LOG.md" in call["args"]["file_path"] for call in edit_file_calls)
```

## 3. Implementation Order

1.  **Templates:** Create the Jinja2 templates for the mock server and tests.
2.  **`PluginFactory`:** Implement the `PluginFactory` class and write unit tests to ensure it correctly generates the full directory structure and file content from a sample profile.
3.  **`EvaluationHarness`:** Implement the `EvaluationHarness` class.
4.  **First Evaluation Test:** Create the `test_playbook_fix_bug.py` file. This will be the final integration test that proves the entire system (Factory, Orchestrator, Agent, and Evaluation) works together.

## 4. Best Practices Applied

-   **Testability:** The entire system is designed around testability. The `EvaluationHarness` is a formalization of this, providing a clean API for end-to-end testing.
-   **SOLID:** The `PluginFactory` and `EvaluationHarness` have single, well-defined responsibilities.
-   **Dependency Injection:** The `EvaluationHarness` takes an `Orchestrator` instance as a dependency, making it easy to configure and test.
-   **Declarative Testing:** The evaluation tests are declarative. They describe the *expected sequence of events* rather than the implementation details, making them robust to refactoring.
