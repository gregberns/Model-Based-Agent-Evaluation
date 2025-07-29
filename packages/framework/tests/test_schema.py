# packages/framework/tests/test_schema.py

import pytest
from pydantic import ValidationError
from packages.framework.schema import PluginProfile

def get_valid_profile_data():
    """Returns a dictionary with valid data for a PluginProfile."""
    return {
        "name": "Test-Plugin",
        "version": "1.2.3",
        "description": "A test plugin.",
        "mcp_profile": [
            {
                "name": "test_tool",
                "description": "A test tool.",
                "parameters": {
                    "param1": {"type": "string", "description": "A test parameter."}
                },
                "output": {"type": "string", "description": "A test output."}
            }
        ],
        "dependencies": ["python:pytest"],
        "configuration": [
            {"name": "TEST_VAR", "description": "A test env var.", "default": "test_value"}
        ],
        "behavioral_profile": {
            "success_scenarios": [
                {
                    "description": "A success scenario.",
                    "tool_call": "test_tool",
                    "inputs": {"param1": "value"},
                    "expected_log": "INFO: Success"
                }
            ],
            "failure_scenarios": []
        }
    }

def test_valid_profile_parses_successfully():
    """Tests that a valid profile dictionary is parsed without errors."""
    data = get_valid_profile_data()
    try:
        PluginProfile(**data)
    except ValidationError as e:
        pytest.fail(f"Valid profile data failed to parse: {e}")

def test_missing_required_field_raises_error():
    """Tests that missing a required field raises a ValidationError."""
    data = get_valid_profile_data()
    del data["name"]
    with pytest.raises(ValidationError):
        PluginProfile(**data)

def test_invalid_semantic_version_raises_error():
    """Tests that an invalid version string raises a ValidationError."""
    data = get_valid_profile_data()
    
    invalid_versions = ["1.0", "1", "1.0.a", "v1.0.0"]
    for version in invalid_versions:
        data["version"] = version
        with pytest.raises(ValidationError) as excinfo:
            PluginProfile(**data)
        assert "Version must be in semantic versioning format" in str(excinfo.value)

def test_optional_fields_can_be_omitted():
    """Tests that optional fields can be omitted without causing an error."""
    data = get_valid_profile_data()
    del data["dependencies"]
    del data["configuration"]
    del data["behavioral_profile"]
    try:
        PluginProfile(**data)
    except ValidationError as e:
        pytest.fail(f"Profile with omitted optional fields failed to parse: {e}")

def test_empty_mcp_profile_is_valid():
    """Tests that an empty mcp_profile list is considered valid."""
    data = get_valid_profile_data()
    data["mcp_profile"] = []
    try:
        PluginProfile(**data)
    except ValidationError as e:
        pytest.fail(f"Profile with empty mcp_profile failed to parse: {e}")
