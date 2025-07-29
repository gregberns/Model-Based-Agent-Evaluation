# 03 - Agent Playbooks: Technical Specification

This document provides the detailed technical specification for the components that load, parse, and prepare Agent Playbooks for execution.

## 1. Architecture and Design

Playbooks are treated as static assets. The technical implementation focuses on the modules responsible for interacting with them: the `PlaybookLoader` and the `PromptConstructor`. These will be simple, robust classes with no external dependencies beyond standard Python libraries.

## 2. File and Class Structure

The implementation will be located within the `packages/framework` directory.

```
/packages/framework/
├── __init__.py
├── loaders.py          # Contains PlaybookLoader.
├── prompt_constructor.py # Contains PromptConstructor.
└── tests/
    ├── test_loaders.py
    └── test_prompt_constructor.py

/playbooks/
└── playbook_fix_bug.md # Example playbook asset.
```

### 2.1. `loaders.py` - PlaybookLoader Class

This class is responsible for loading a playbook file and parsing its content into a structured object.

```python
# packages/framework/loaders.py

from pathlib import Path
from pydantic import BaseModel

class Playbook(BaseModel):
    """A simple data class to hold the parsed playbook content."""
    objective: str
    prompt_template: str

class PlaybookLoader:
    """Loads and parses a playbook.md file."""

    def load(self, playbook_path: Path) -> Playbook:
        """
        Loads a playbook from a given path.

        Args:
            playbook_path: The path to the playbook markdown file.

        Returns:
            A Playbook object with the parsed content.
        """
        if not playbook_path.is_file():
            raise FileNotFoundError(f"Playbook not found at {playbook_path}")

        content = playbook_path.read_text()
        
        # A simple parsing logic based on markdown headers.
        # This could be made more robust if needed.
        try:
            objective_section = content.split("## Objective")[1].split("##")[0].strip()
            prompt_section = content.split("## Contextual Prompt Template")[1].strip()
        except IndexError:
            raise ValueError(f"Playbook {playbook_path} is missing required sections.")

        return Playbook(objective=objective_section, prompt_template=prompt_section)
```

### 2.2. `prompt_constructor.py` - PromptConstructor Class

This class takes the loaded playbook and plugin profile and constructs the final, contextualized prompt to be sent to the agent.

```python
# packages/framework/prompt_constructor.py

from .loaders import Playbook
from .schema import PluginProfile

class PromptConstructor:
    """Constructs the initial prompt for the agent."""

    def construct(self, playbook: Playbook, profile: PluginProfile, env: str, **kwargs) -> str:
        """
        Constructs the final prompt string.

        Args:
            playbook: The loaded playbook.
            profile: The loaded plugin profile.
            env: The environment ('virtual' or 'real').
            **kwargs: Additional placeholder values (e.g., bug_description).

        Returns:
            The fully rendered prompt string.
        """
        prompt = playbook.prompt_template

        # Basic placeholders
        prompt = prompt.replace("{environment}", env.title())
        prompt = prompt.replace("{working_directory}", f"./{profile.name}") # Example
        
        for key, value in kwargs.items():
            prompt = prompt.replace(f"{{{key}}}", value)

        # Environment-specific instructions
        if env == 'virtual':
            instructions = "To modify the behavior of a Virtual Plugin, you must edit the `plugin-profile.yaml` file."
        else: # env == 'real'
            instructions = "To fix this bug, you must modify the source code in the `src/` directory."
        
        prompt = prompt.replace("{environment_specific_instructions}", instructions)

        return prompt
```

## 3. Implementation Order

1.  **`PlaybookLoader`:**
    -   Implement the `Playbook` data class and the `PlaybookLoader` class.
    -   Write `tests/test_loaders.py`. Tests should:
        -   Verify successful loading and parsing of a valid playbook file.
        -   Assert that `FileNotFoundError` is raised for a missing file.
        -   Assert that `ValueError` is raised for a malformed playbook.
2.  **`PromptConstructor`:**
    -   Implement the `PromptConstructor` class.
    -   Write `tests/test_prompt_constructor.py`. Tests should:
        -   Verify that all placeholders are correctly replaced for both `virtual` and `real` environments.
        -   Verify that additional `kwargs` are correctly injected.

## 4. Best Practices Applied

-   **Library First:** Both `PlaybookLoader` and `PromptConstructor` are stateless, reusable classes that can be used in any context.
-   **Solid Abstractions:** The complexity of finding, reading, parsing, and templating files is hidden behind simple `load()` and `construct()` methods.
-   **Testability:** Both classes are pure Python and have no external dependencies, making them trivial to unit test.
-   **DRY Principle:** The logic for loading and parsing playbooks is centralized in one place. The logic for prompt construction is also centralized.
