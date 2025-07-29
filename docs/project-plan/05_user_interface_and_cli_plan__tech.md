# 05 - User Interface and CLI: Technical Specification

This document provides the detailed technical specification for the user-facing command-line interface.

## 1. Architecture and Design

The UI will be implemented in two layers, following the plan:
1.  **Core CLI (`__main__.py`):** A Python script using the `argparse` library to provide a structured, command-based interface to the framework's library functions.
2.  **`Makefile`:** A simple wrapper around the core CLI to provide convenient, memorable shortcuts for the most common development and execution workflows.

Development of these components is **deferred** until the core libraries (`Orchestrator`, `PluginFactory`, `EvaluationHarness`) are complete and tested.

## 2. File and Class Structure

```
/packages/framework/
├── __main__.py         # The main CLI entrypoint.

/Makefile               # The developer-facing command shortcuts.
```

### 2.1. `__main__.py` - Core CLI

This script will be the single entrypoint for all command-line operations.

```python
# packages/framework/__main__.py

import argparse
from pathlib import Path
# ... other necessary imports from the framework

def main():
    parser = argparse.ArgumentParser(description="Plugin Manager Framework CLI")
    subparsers = parser.add_subparsers(dest="action", required=True)

    # --- Generate Action ---
    parser_generate = subparsers.add_parser("generate", help="Generate a virtual plugin.")
    parser_generate.add_argument("--profile-path", type=Path, required=True, help="Path to the plugin profile YAML file.")
    parser_generate.add_argument("--output-dir", type=Path, default=Path("./plugins_virtual"), help="Directory to generate the plugin in.")

    # --- Run Action ---
    parser_run = subparsers.add_parser("run", help="Run a playbook on a plugin.")
    parser_run.add_argument("--playbook-path", type=Path, required=True, help="Path to the playbook markdown file.")
    parser_run.add_argument("--plugin-path", type=Path, required=True, help="Path to the plugin directory.")
    parser_run.add_argument("--env", choices=['virtual', 'real'], required=True, help="The execution environment.")
    parser_run.add_argument("--bug-description", type=str, help="Bug description for the fix_bug playbook.")
    parser_run.add_argument("--yes", action="store_true", help="Bypass human-in-the-loop confirmations.")


    args = parser.parse_args()

    # (This is where the logic to instantiate and call the library classes will go)
    if args.action == "generate":
        # Instantiate and call PluginFactory
        pass
    elif args.action == "run":
        # Instantiate and call Orchestrator
        pass

if __name__ == "__main__":
    main()
```

### 2.2. `Makefile`

The `Makefile` will translate simple commands into the more verbose `python -m framework` calls.

```makefile
# Makefile

# Default values, can be overridden from the command line
# e.g., make run-playbook PLAYBOOK=tdd PLUGIN=my-plugin
PLAYBOOK ?= fix_bug
PLUGIN   ?= image-processor
ENV      ?= virtual

.PHONY: help setup test-framework test-playbooks generate-virtual-plugin run-playbook

# ... (help, setup, test targets as defined previously) ...

generate-virtual-plugin:
	python -m framework generate --profile-path ./plugins_virtual/$(PLUGIN)/plugin-profile.yaml

run-playbook:
	python -m framework run \
		--playbook-path ./playbooks/playbook_$(PLAYBOOK).md \
		--plugin-path ./plugins_$(ENV)/$(PLUGIN) \
		--env $(ENV)
```

## 3. Implementation Order

1.  **Core Library First:** This entire module will be implemented *after* the core framework libraries are complete and stable.
2.  **`__main__.py`:** Implement the `argparse` structure and the logic to call the underlying library classes.
3.  **`Makefile`:** Create the `Makefile` with the command shortcuts.

## 4. Best Practices Applied

-   **Separation of Concerns:** The `Makefile` is a convenience layer, while the `__main__.py` script contains the actual CLI logic. This is a standard and robust pattern.
-   **Library First:** The CLI is a thin wrapper around the core library. All the complex logic resides in the library, making the CLI simple and easy to maintain.
-   **Discoverability:** The `Makefile`'s `help` target and `argparse`'s `--help` flags make the system's capabilities easily discoverable for developers.
