# packages/framework/factory.py

import shutil
from pathlib import Path
import yaml
from jinja2 import Environment, FileSystemLoader
from .schema import PluginProfile

class PluginFactory:
    """Generates a virtual plugin from a profile."""

    def __init__(self, template_dir: Path):
        self.template_env = Environment(loader=FileSystemLoader(template_dir))

    def create(self, profile_path: Path, output_dir: Path) -> Path:
        """
        Creates the virtual plugin directory structure and files.

        Args:
            profile_path: Path to the plugin-profile.yaml.
            output_dir: The root directory where the plugin will be created.

        Returns:
            The path to the newly created plugin directory.
        """
        with open(profile_path, 'r') as f:
            profile_data = yaml.safe_load(f)
            profile = PluginProfile(**profile_data)

        plugin_path = output_dir / profile.name
        if plugin_path.exists():
            shutil.rmtree(plugin_path)  # Ensure a clean slate
        
        # Create directories
        src_path = plugin_path / "src"
        tests_path = plugin_path / "tests"
        history_path = plugin_path / ".history"
        src_path.mkdir(parents=True)
        tests_path.mkdir()
        history_path.mkdir()

        # Write the profile back to the new directory
        shutil.copy(profile_path, plugin_path / "plugin-profile.yaml")

        # Generate mock server from template
        main_template = self.template_env.get_template("virtual_main.py.j2")
        main_content = main_template.render(profile=profile.model_dump())
        (src_path / "main.py").write_text(main_content)

        # Generate mock tests from template
        test_template = self.template_env.get_template("virtual_test.py.j2")
        test_content = test_template.render(profile=profile)
        (tests_path / "test_virtual.py").write_text(test_content)
        
        return plugin_path
