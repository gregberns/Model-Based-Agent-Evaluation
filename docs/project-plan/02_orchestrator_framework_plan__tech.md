# 02 - Orchestrator Framework: Technical Specification

This document provides the detailed technical specification for implementing the Orchestrator framework.

## 1. Architecture and Design

The Orchestrator is designed as a modular, event-driven library. Its core responsibility is to manage the execution of a playbook by mediating the conversation between an Agent and a set of observable Tools.

-   **Composability:** The framework will be built from small, single-responsibility classes (`ProfileLoader`, `PlaybookLoader`, `PromptConstructor`, `Orchestrator`) that are composed together at runtime.
-   **Event-Driven:** A simple pub/sub event system will be used to decouple the core execution logic from observability concerns like logging. This allows new listeners (e.g., for testing, UI updates) to be added without modifying the core orchestrator.
-   **Tool Wrapping:** Tools will be wrapped using a decorator or a simple wrapper class to ensure all tool calls emit events before and after execution.

## 2. File and Class Structure

```
/packages/framework/
├── __init__.py
├── orchestrator.py     # The main Orchestrator class and execution loop.
├── events.py           # The event emitter and event data structures.
├── tool_wrapper.py     # The decorator/class for wrapping tools.
├── loaders.py          # Contains ProfileLoader and PlaybookLoader.
├── prompt_constructor.py # Logic for building the initial prompt.
└── tests/
    ├── test_orchestrator.py
    ├── test_events.py
    └── test_tool_wrapper.py
```

### 2.1. `events.py` - Event System

A simple, in-memory pub/sub system.

```python
# packages/framework/events.py

from typing import Callable, Dict, Any, List

class EventEmitter:
    def __init__(self):
        self._listeners: Dict[str, List[Callable]] = {}

    def on(self, event_name: str, listener: Callable):
        if event_name not in self._listeners:
            self._listeners[event_name] = []
        self._listeners[event_name].append(listener)

    def emit(self, event_name: str, data: Dict[str, Any]):
        if event_name in self._listeners:
            for listener in self._listeners[event_name]:
                listener(data)

# Global event emitter instance
event_emitter = EventEmitter()
```

### 2.2. `tool_wrapper.py` - Tool Wrapper

This module will provide a function to wrap the agent's tools for observability.

```python
# packages/framework/tool_wrapper.py

from functools import wraps
from .events import event_emitter

def wrap_tool(tool_function: Callable) -> Callable:
    """Decorator to wrap a tool function for event emission."""
    @wraps(tool_function)
    def wrapper(*args, **kwargs):
        tool_name = tool_function.__name__
        event_data = {"name": tool_name, "args": kwargs}
        
        event_emitter.emit("tool_requested", event_data)
        
        try:
            result = tool_function(*args, **kwargs)
            event_emitter.emit("tool_completed", {**event_data, "result": result})
            return result
        except Exception as e:
            event_emitter.emit("tool_failed", {**event_data, "error": str(e)})
            raise  # Re-raise the exception after logging
            
    return wrapper
```

### 2.3. `orchestrator.py` - Orchestrator Class

The core engine that runs the playbook.

```python
# packages/framework/orchestrator.py

from .loaders import ProfileLoader, PlaybookLoader
from .prompt_constructor import PromptConstructor
from packages.plugin_manager_agent import GeminiAgent

class Orchestrator:
    def __init__(self, agent: GeminiAgent, profile_loader: ProfileLoader, playbook_loader: PlaybookLoader, prompt_constructor: PromptConstructor):
        self.agent = agent
        self.profile_loader = profile_loader
        # ... and so on

    def run(self, playbook_path: Path, plugin_path: Path, env: str, bug_description: str = ""):
        """Main execution method."""
        # 1. Load profile and playbook
        profile = self.profile_loader.load(plugin_path)
        playbook = self.playbook_loader.load(playbook_path)

        # 2. Construct the initial prompt
        prompt = self.prompt_constructor.construct(
            playbook=playbook,
            profile=profile,
            env=env,
            bug_description=bug_description
        )

        # 3. Run the agent's execution generator
        execution_generator = self.agent.execute(prompt)
        
        final_response = None
        try:
            while True:
                tool_call = next(execution_generator)
                # The agent's internal tool execution will trigger our wrapped tools,
                # which in turn emit events. The orchestrator doesn't need to do
                # anything special here because the wrapping is handled at agent
                # instantiation.
        except StopIteration as e:
            final_response = e.value
        
        return final_response
```

## 3. Implementation Order

1.  **Event System:** Implement the `EventEmitter` in `events.py` and write unit tests for it.
2.  **Tool Wrapper:** Implement the `wrap_tool` decorator in `tool_wrapper.py`. Write unit tests to ensure it correctly emits `tool_requested`, `tool_completed`, and `tool_failed` events.
3.  **Composable Loaders:** Implement the `ProfileLoader` (from previous spec) and `PlaybookLoader` classes in `loaders.py`.
4.  **Prompt Constructor:** Implement the `PromptConstructor` class.
5.  **Orchestrator Class:** Implement the `Orchestrator` class, integrating all the components. Its unit tests will involve mocking the `GeminiAgent` to ensure the `run` method correctly calls its dependencies and handles the generator flow.

## 4. Best Practices Applied

-   **Library First & Composability:** The entire framework is designed as a set of classes that can be imported and used independently or composed together for the full workflow.
-   **Solid Abstractions:** The event system is a classic example of the Observer pattern, decoupling the core logic from logging. The `Orchestrator` class uses Dependency Injection in its constructor, making it highly testable.
-   **Testability:** Each component (`EventEmitter`, `ToolWrapper`, `Orchestrator`) is small, has a single responsibility, and can be unit-tested in isolation. Mocks will be needed for testing the `Orchestrator`'s interaction with the agent, but the dependencies are explicit.
