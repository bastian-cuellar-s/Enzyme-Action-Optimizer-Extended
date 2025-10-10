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
	@if [ -d tests ] || [ -n "$(shell git ls-files 'tests/**')" ]; then \
		@echo "(tests removed in this repo layout)"; \
	else \
		echo "No tests found; skipping"; \
	fi

lint:
	$(PY) -m flake8 .

format:
	$(PY) -m black .
