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
	.venv/bin/pytest

run-plugin:
	@./scripts/run_plugin.sh "$(p)" "$(pb)" "$(bug)"


# ==============================================================================
# UTILITY
# ==============================================================================

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
