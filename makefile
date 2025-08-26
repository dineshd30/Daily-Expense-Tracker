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

freeze:
	@pip freeze > requirements.txt
	@echo "✅ Requirements frozen to requirements.txt"

install:
	@pip install -r requirements.txt
	@echo "✅ Packages installed from requirements.txt"
