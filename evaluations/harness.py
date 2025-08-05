# evaluations/harness.py

from typing import List, Dict, Any, Callable, Optional
from packages.framework.orchestrator import Orchestrator
from packages.framework.events import event_emitter
from packages.framework.utils import get_gemini_api_key

class EvaluationHarness:
    """Runs a playbook and captures events for assertion."""

    def __init__(self, orchestrator: Orchestrator):
        self.orchestrator = orchestrator
        self.captured_events: List[Dict[str, Any]] = []

    def _event_listener(self, data: Dict[str, Any]):
        """Appends captured events to the internal list."""
        self.captured_events.append(data)

    def run_and_capture(self, api_key: Optional[str] = None, *args, **kwargs) -> List[Dict[str, Any]]:
        """
        Runs the orchestrator and captures all emitted events.

        Args:
            api_key: Gemini API key. If None, will be loaded from environment or .env files.
        """
        # Get API key using the utility function
        try:
            resolved_api_key = get_gemini_api_key(api_key)
        except ValueError as e:
            # Convert to RuntimeError for consistency with test framework expectations
            raise RuntimeError(f"API key error: {e}")

        # Update kwargs with the resolved API key
        kwargs['api_key'] = resolved_api_key

        self.captured_events = [] # Reset

        # Register a generic listener for all events.
        # A more robust implementation might allow selective listening.
        def generic_listener(data):
            self._event_listener(data)

        # A simple way to listen to all events without knowing their names
        # would be to modify the emitter, but for now, we'll be explicit.
        event_emitter.on("tool_requested", generic_listener)
        event_emitter.on("tool_completed", generic_listener)
        event_emitter.on("tool_failed", generic_listener)

        # The orchestrator now runs to completion in a single call.
        # Events are captured by the listener registered to the global emitter.
        final_response = self.orchestrator.run(*args, **kwargs)

        # Unregister the listener to avoid side effects in other tests
        event_emitter.remove_listener("tool_requested", generic_listener)
        event_emitter.remove_listener("tool_completed", generic_listener)
        event_emitter.remove_listener("tool_failed", generic_listener)

        return final_response
