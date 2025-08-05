.PHONY: help test clean install-deps run-plugin

# ==============================================================================
# HELP
# ==============================================================================

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  install-deps   Install python dependencies from requirements.txt"
	@echo "  test           Run all unit and evaluation tests"
	@echo "  run-plugin     Run a playbook on a real plugin. Ex: make run-plugin p=my-first-plugin pb=playbook_fix_bug bug='Fix whitespace issue'"
	@echo "  clean          Remove temporary Python files"


# ==============================================================================
# DEVELOPMENT
# ==============================================================================

install-deps:
	.venv/bin/pip install -r requirements.txt

test:
	@echo "Running tests..."
	@echo ""
	@echo "Deterministic Tests (Unit/Integration):"
	@echo "  pytest evaluations/deterministic/ -v"
	@echo ""
	@echo "Agent/Playbook Tests (End-to-End):"
	@echo "  pytest evaluations/agent/ -v"
	@echo ""
	@echo "All Tests:"
	.venv/bin/pytest

run-plugin:
	@echo "Running playbook on real plugin..."
	@echo ""
	@echo "Usage: make run-plugin p=<plugin_name> pb=<playbook_name> [bug='<description>']"
	@echo ""
	@echo "Parameters:"
	@echo "  p     - Name of the plugin to operate on (required)"
	@echo "  pb    - Name of the playbook to execute (required, without .md extension)"
	@echo "  bug   - Optional bug description for the playbook context"
	@echo ""
	@echo "Examples:"
	@echo "  make run-plugin p=my-first-plugin pb=playbook_fix_bug"
	@echo "  make run-plugin p=my-first-plugin pb=playbook_fix_bug bug='Fix whitespace issue in main.py'"
	@echo "  make run-plugin p=web-server pb=playbook_update_version bug='Update to version 2.0.0'"
	@echo ""
	@echo "Available Playbooks:"
	@ls -1 playbooks/*.md | sed 's/\.md$//' | sed 's/playbook_/- /' | sed 's/^/  /'
	@echo ""
	@echo "Note: This command uses the real plugin environment and requires GEMINI_API_KEY to be set."
	@echo "      For virtual plugin testing, use the evaluation harness directly."
	@echo ""
	@./scripts/run_plugin.sh "$(p)" "$(pb)" "$(bug)"


# ==============================================================================
# UTILITY
# ==============================================================================

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
