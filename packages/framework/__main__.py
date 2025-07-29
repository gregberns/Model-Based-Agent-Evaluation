# packages/framework/__main__.py

import argparse
import os
from pathlib import Path
import logging

# Add the project root to the Python path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from packages.framework.orchestrator import Orchestrator
from packages.framework.loaders import ProfileLoader, PlaybookLoader
from packages.framework.prompt_constructor import PromptConstructor

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """The main entrypoint for the CLI."""
    parser = argparse.ArgumentParser(description="Plugin Manager Agent CLI")
    parser.add_argument("plugin_name", help="The name of the plugin to operate on (must be in /plugins_real).")
    parser.add_argument("playbook_name", help="The name of the playbook to run (e.g., 'playbook_fix_bug').")
    parser.add_argument("--bug", help="The description of the bug to fix.", default="")
    parser.add_argument("--hitl", action="store_true", help="Enable Human-in-the-Loop confirmation for destructive tools.")
    
    args = parser.parse_args()

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        sys.exit(1)

    # Construct paths
    project_root = Path(__file__).parent.parent.parent
    plugin_path = project_root / "plugins_real" / args.plugin_name
    playbook_path = project_root / "playbooks" / f"{args.playbook_name}.md"

    if not plugin_path.is_dir():
        print(f"Error: Plugin '{args.plugin_name}' not found at {plugin_path}")
        sys.exit(1)
    
    if not playbook_path.is_file():
        print(f"Error: Playbook '{args.playbook_name}' not found at {playbook_path}")
        sys.exit(1)

    # Instantiate the orchestrator
    orchestrator = Orchestrator(
        profile_loader=ProfileLoader(),
        playbook_loader=PlaybookLoader(),
        prompt_constructor=PromptConstructor(),
        hitl=args.hitl
    )

    # Run the orchestrator
    print(f"Running playbook '{args.playbook_name}' on plugin '{args.plugin_name}'...")
    final_response = orchestrator.run(
        playbook_path=playbook_path,
        plugin_path=plugin_path,
        env="real",
        api_key=api_key,
        bug_description=args.bug
    )

    print("\n--- Agent's Final Response ---")
    print(final_response)
    print("----------------------------\n")

if __name__ == "__main__":
    main()