# Makefile

# Check if a virtual environment exists
VENV_NAME := .venv
VENV_ACTIVATE := $(VENV_NAME)/bin/activate
VENV_PYTHON := $(VENV_NAME)/bin/python

# Define the lint:scan target
lint\:scan:
	@if [ -f $(VENV_ACTIVATE) ]; then \
		source $(VENV_ACTIVATE); \
		pylint .; \
	else \
		pylint .; \
	fi

.PHONY: lint\:scan