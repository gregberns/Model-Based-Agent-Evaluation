# packages/framework/events.py

from typing import Callable, Dict, Any, List

class EventEmitter:
    """A simple in-memory pub/sub event emitter."""
    def __init__(self):
        self._listeners: Dict[str, List[Callable]] = {}

    def on(self, event_name: str, listener: Callable):
        """Register a listener for a given event."""
        if event_name not in self._listeners:
            self._listeners[event_name] = []
        self._listeners[event_name].append(listener)

    def emit(self, event_name: str, data: Dict[str, Any]):
        """Emit an event to all registered listeners."""
        if event_name in self._listeners:
            for listener in self._listeners[event_name]:
                listener(data)

    def remove_listener(self, event_name: str, listener_to_remove: Callable):
        """Remove a specific listener for a given event."""
        if event_name in self._listeners:
            self._listeners[event_name] = [
                listener for listener in self._listeners[event_name]
                if listener != listener_to_remove
            ]

# A global singleton instance for the application to use.
event_emitter = EventEmitter()