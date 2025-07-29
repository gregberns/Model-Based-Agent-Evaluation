# packages/framework/tests/test_factory.py

import pytest
import yaml
from pathlib import Path
from packages.framework.factory import PluginFactory
from packages.framework.schema import PluginProfile

@pytest.fixture
def sample_profile_path(tmp_path: Path) -> Path:
    """Creates a sample plugin-profile.yaml for testing."""
    profile_data = {
        "name": "Test-Plugin",
        "version": "1.0.0",
        "description": "A test plugin.",
        "mcp_profile": [],
        "behavioral_profile": {
            "success_scenarios": [
                {
                    "description": "A success scenario.",
                    "tool_call": "test_tool",
                    "inputs": {"param1": "value"},
                    "expected_log": "INFO: Success"
                }
            ],
            "failure_scenarios": [
                {
                    "description": "A failure scenario.",
                    "tool_call": "fail_tool",
                    "inputs": {},
                    "expected_log": "ERROR: Failure"
                }
            ]
        }
    }
    profile_path = tmp_path / "sample-profile.yaml"
    with open(profile_path, 'w') as f:
        yaml.dump(profile_data, f)
    return profile_path

def test_plugin_factory_creates_directory_structure(sample_profile_path: Path, tmp_path: Path):
    """Tests that the factory creates the correct directory structure."""
    template_dir = Path(__file__).parent.parent.parent.parent / "templates"
    factory = PluginFactory(template_dir=template_dir)
    
    output_dir = tmp_path / "output"
    plugin_path = factory.create(sample_profile_path, output_dir)

    assert plugin_path.exists()
    assert (plugin_path / "plugin-profile.yaml").is_file()
    assert (plugin_path / "src").is_dir()
    assert (plugin_path / "src/main.py").is_file()
    assert (plugin_path / "tests").is_dir()
    assert (plugin_path / "tests/test_virtual.py").is_file()
    assert (plugin_path / ".history").is_dir()

def test_plugin_factory_generates_correct_files(sample_profile_path: Path, tmp_path: Path):
    """Tests that the generated files have the correct content."""
    template_dir = Path(__file__).parent.parent.parent.parent / "templates"
    factory = PluginFactory(template_dir=template_dir)
    
    output_dir = tmp_path / "output"
    plugin_path = factory.create(sample_profile_path, output_dir)

    # Check main.py content
    main_py_content = (plugin_path / "src/main.py").read_text()
    assert 'if __name__ == "__main__":' in main_py_content
    assert 'success_scenarios' in main_py_content

    # Check test_virtual.py content
    test_py_content = (plugin_path / "tests/test_virtual.py").read_text()
    assert "def test_success_1():" in test_py_content
    assert '"""Tests the success scenario: A success scenario."""' in test_py_content
    assert "def test_failure_1():" in test_py_content
    assert '"""Tests the failure scenario: A failure scenario."""' in test_py_content
