.PHONY: install run-poc activate

install:
	uv pip install -r requirements.txt

run-poc:
	python -m packages.agent_poc.main

run-poc-aider:
	python -m packages.agent_poc.try_aider

activate:
	. .venv/bin/activate
