# packages/framework/tests/test_events.py

import pytest
from packages.framework.events import EventEmitter

def test_event_emitter_can_register_and_emit_event():
    """Tests that a listener can be registered and is called on emit."""
    emitter = EventEmitter()
    
    # A simple listener that appends data to a list
    received_data = []
    def listener(data):
        received_data.append(data)

    emitter.on("test_event", listener)
    
    test_payload = {"key": "value"}
    emitter.emit("test_event", test_payload)

    assert len(received_data) == 1
    assert received_data[0] == test_payload

def test_event_emitter_multiple_listeners():
    """Tests that multiple listeners can be registered for the same event."""
    emitter = EventEmitter()
    
    listener1_called = False
    def listener1(data):
        nonlocal listener1_called
        listener1_called = True

    listener2_called = False
    def listener2(data):
        nonlocal listener2_called
        listener2_called = True

    emitter.on("test_event", listener1)
    emitter.on("test_event", listener2)
    
    emitter.emit("test_event", {})

    assert listener1_called
    assert listener2_called

def test_event_emitter_no_listeners_for_event():
    """Tests that emitting an event with no listeners does not cause an error."""
    emitter = EventEmitter()
    try:
        emitter.emit("unheard_event", {})
    except Exception as e:
        pytest.fail(f"Emitting an event with no listeners raised an exception: {e}")

def test_event_emitter_multiple_events():
    """Tests that the emitter correctly handles multiple, distinct events."""
    emitter = EventEmitter()

    event1_data = []
    def listener1(data):
        event1_data.append(data)

    event2_data = []
    def listener2(data):
        event2_data.append(data)

    emitter.on("event1", listener1)
    emitter.on("event2", listener2)

    emitter.emit("event1", {"source": "event1"})
    
    assert len(event1_data) == 1
    assert event1_data[0] == {"source": "event1"}
    assert len(event2_data) == 0

    emitter.emit("event2", {"source": "event2"})

    assert len(event1_data) == 1
    assert len(event2_data) == 1
    assert event2_data[0] == {"source": "event2"}
