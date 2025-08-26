# Makefile for Python dependencies

.PHONY: venv freeze install

# Name of your virtual environment folder
VENV := venv

venv:
	@echo "🐍 Checking virtual environment..."
	@if [ ! -d "$(VENV)" ]; then \
		echo "🚀 Creating virtual environment..."; \
		python -m venv $(VENV); \
	else \
		echo "✅ Virtual environment already exists."; \
	fi
	@bash -i -c "source $(VENV)/bin/activate"
	@echo "✅ Activated virtual environment"

install: venv
	@poetry install
	@echo "✅ Packages installed via poetry"
