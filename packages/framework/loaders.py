# packages/framework/loaders.py

import yaml
from pathlib import Path
from pydantic import BaseModel, ValidationError
from .schema import PluginProfile

class Playbook(BaseModel):
    """A simple data class to hold the parsed playbook content."""
    objective: str
    prompt_template: str

class ProfileLoader:
    """Loads and validates a plugin-profile.yaml file."""

    def load(self, plugin_directory: Path) -> PluginProfile:
        """
        Finds and loads the plugin profile from a given directory.

        Args:
            plugin_directory: The root directory of the plugin.

        Returns:
            A validated PluginProfile object.

        Raises:
            FileNotFoundError: If plugin-profile.yaml is not found.
            ValidationError: If the profile is invalid.
        """
        profile_path = plugin_directory / "plugin-profile.yaml"
        if not profile_path.is_file():
            raise FileNotFoundError(f"plugin-profile.yaml not found in {plugin_directory}")

        with open(profile_path, 'r') as f:
            data = yaml.safe_load(f)
            try:
                profile = PluginProfile(**data)
                return profile
            except ValidationError as e:
                # Re-raise to be handled by the caller
                raise e

class PlaybookLoader:
    """Loads and parses a playbook.md file."""

    def load(self, playbook_path: Path) -> Playbook:
        """
        Loads a playbook from a given path.

        Args:
            playbook_path: The path to the playbook markdown file.

        Returns:
            A Playbook object with the parsed content.
        """
        if not playbook_path.is_file():
            raise FileNotFoundError(f"Playbook not found at {playbook_path}")

        content = playbook_path.read_text()
        
        try:
            # A simple parsing logic based on markdown headers.
            objective_section = content.split("## Objective")[1].split("##")[0].strip()
            prompt_section = content.split("## Contextual Prompt Template")[1].strip()
        except IndexError:
            raise ValueError(f"Playbook {playbook_path} is missing required sections.")

        return Playbook(objective=objective_section, prompt_template=prompt_section)
