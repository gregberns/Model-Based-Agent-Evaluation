# packages/framework/tool_wrapper.py

from functools import wraps
from typing import Callable
from .events import event_emitter

def tool_wrapper_factory(hitl: bool = False):
    """
    A factory that returns a decorator to wrap a tool function for event emission
    and optional Human-in-the-Loop confirmation.
    """
    def wrap_tool(tool_function: Callable) -> Callable:
        """
        Decorator to wrap a tool function.
        """
        @wraps(tool_function)
        def wrapper(*args, **kwargs):
            tool_name = tool_function.__name__
            
            arg_names = tool_function.__code__.co_varnames[:tool_function.__code__.co_argcount]
            all_args = {**dict(zip(arg_names, args)), **kwargs}

            event_data = {"name": tool_name, "args": all_args}
            
            # Check for HITL confirmation if the tool is destructive
            if hitl and tool_name in ["edit_file", "execute_shell_command"]:
                print("\n--- HUMAN-IN-THE-LOOP ---")
                print(f"Agent wants to execute tool: {tool_name}")
                print("Arguments:")
                for key, value in all_args.items():
                    print(f"  {key}: {value}")
                
                confirmation = input("Approve? (y/n): ")
                if confirmation.lower() != 'y':
                    print("Execution rejected by user.")
                    # We'll treat this as a failure, as the agent's plan was interrupted
                    error_message = "Tool execution rejected by user."
                    event_emitter.emit("tool_failed", {**event_data, "error": error_message})
                    raise RuntimeError(error_message)
                
                print("Execution approved.")
                print("-------------------------\n")

            event_emitter.emit("tool_requested", event_data)
            
            try:
                result = tool_function(*args, **kwargs)
                event_emitter.emit("tool_completed", {**event_data, "result": result})
                return result
            except Exception as e:
                event_emitter.emit("tool_failed", {**event_data, "error": str(e)})
                raise
                
        return wrapper
    return wrap_tool