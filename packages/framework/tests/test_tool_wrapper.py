# packages/framework/tests/test_tool_wrapper.py

import pytest
from packages.framework.events import EventEmitter
from packages.framework.tool_wrapper import wrap_tool

@pytest.fixture
def emitter():
    """Provides a clean EventEmitter instance for each test."""
    return EventEmitter()

def test_wrap_tool_emits_requested_and_completed_events(emitter):
    """Tests that the wrapper emits success events correctly."""
    
    @wrap_tool
    def sample_tool(param1: str, param2: int = 10):
        return f"Success with {param1} and {param2}"

    captured_events = []
    def listener(data):
        captured_events.append(data)

    emitter.on("tool_requested", listener)
    emitter.on("tool_completed", listener)

    # Replace the global emitter with our test instance
    import packages.framework.tool_wrapper as tool_wrapper_module
    original_emitter = tool_wrapper_module.event_emitter
    tool_wrapper_module.event_emitter = emitter
    
    result = sample_tool(param1="test")

    # Restore the original emitter
    tool_wrapper_module.event_emitter = original_emitter

    assert result == "Success with test and 10"
    assert len(captured_events) == 2
    
    requested_event = captured_events[0]
    assert requested_event["name"] == "sample_tool"
    assert requested_event["args"] == {"param1": "test"}

    completed_event = captured_events[1]
    assert completed_event["name"] == "sample_tool"
    assert completed_event["args"] == {"param1": "test"}
    assert completed_event["result"] == "Success with test and 10"

def test_wrap_tool_emits_failed_event_on_exception(emitter):
    """Tests that the wrapper emits a failure event and re-raises the exception."""

    @wrap_tool
    def failing_tool():
        raise ValueError("Tool failed")

    captured_events = []
    def listener(data):
        captured_events.append(data)

    emitter.on("tool_requested", listener)
    emitter.on("tool_failed", listener)

    import packages.framework.tool_wrapper as tool_wrapper_module
    original_emitter = tool_wrapper_module.event_emitter
    tool_wrapper_module.event_emitter = emitter

    with pytest.raises(ValueError, match="Tool failed"):
        failing_tool()

    tool_wrapper_module.event_emitter = original_emitter

    assert len(captured_events) == 2
    
    requested_event = captured_events[0]
    assert requested_event["name"] == "failing_tool"
    assert requested_event["args"] == {}

    failed_event = captured_events[1]
    assert failed_event["name"] == "failing_tool"
    assert failed_event["args"] == {}
    assert failed_event["error"] == "Tool failed"
