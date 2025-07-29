# packages/framework/tool_wrapper.py

from functools import wraps
from typing import Callable
from .events import event_emitter

def wrap_tool(tool_function: Callable) -> Callable:
    """
    Decorator to wrap a tool function for event emission.
    It captures the tool name, arguments, result, and any exceptions.
    """
    @wraps(tool_function)
    def wrapper(*args, **kwargs):
        tool_name = tool_function.__name__
        
        # Consolidate arguments for logging
        # This handles both positional and keyword arguments
        arg_names = tool_function.__code__.co_varnames[:tool_function.__code__.co_argcount]
        all_args = {**dict(zip(arg_names, args)), **kwargs}

        event_data = {"name": tool_name, "args": all_args}
        
        event_emitter.emit("tool_requested", event_data)
        
        try:
            result = tool_function(*args, **kwargs)
            event_emitter.emit("tool_completed", {**event_data, "result": result})
            return result
        except Exception as e:
            event_emitter.emit("tool_failed", {**event_data, "error": str(e)})
            # It's important to re-raise the exception so the agent knows the tool failed
            raise
            
    return wrapper
