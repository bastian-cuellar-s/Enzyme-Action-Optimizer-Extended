VENV?=venv
PY=python

.PHONY: setup install test lint format

setup:
	$(PY) -m venv $(VENV)
	@echo "Activate with: source $(VENV)/bin/activate (Unix) or $(VENV)\\Scripts\\Activate.ps1 (PowerShell)"

install:
	$(PY) -m pip install --upgrade pip
	$(PY) -m pip install -r requirements.txt

test:
	@echo "Tests were removed from this repository per maintainer request; no-op."

lint:
	@echo "Lint target is a no-op in the minimal repository. Install flake8 locally if you want to run lint checks."

format:
	$(PY) -m black .
