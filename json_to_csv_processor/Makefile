# Makefile for JSON to CSV Processor

# Python interpreter
PYTHON = python3

# Virtual environment
VENV = venv
VENV_ACTIVATE = . $(VENV)/bin/activate

# Script name
SCRIPT = main.py

# Output file
OUTPUT = output-product.csv

# Test directory
TEST_DIR = tests

# Phony targets
.PHONY: all setup run test clean

# Default target
all: setup test run

# Setup virtual environment and install dependencies
setup:
	@echo "Setting up virtual environment..."
	@$(PYTHON) -m venv $(VENV)
	@$(VENV_ACTIVATE) && pip install --upgrade pip
	@$(VENV_ACTIVATE) && pip install -r requirements.txt

# Run the script
run:
	@echo "Running the script..."
	@$(VENV_ACTIVATE) && $(PYTHON) $(SCRIPT)

# Run tests with coverage
test:
	@echo "Running tests with coverage..."
	@$(VENV_ACTIVATE) && PYTHONPATH=$$PYTHONPATH:. pytest --cov=. $(TEST_DIR) --cov-report=term-missing

# Clean up
clean:
	@echo "Cleaning up..."
	@rm -rf $(VENV)
	@rm -f $(OUTPUT)
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete

# Show help
help:
	@echo "Available targets:"
	@echo "  setup  : Set up virtual environment and install dependencies"
	@echo "  run    : Run the script"
	@echo "  test   : Run unit tests with coverage"
	@echo "  clean  : Remove virtual environment, output file, and Python cache files"
	@echo "  all    : Setup, run tests, and run the script (default)"
	@echo "  help   : Show this help message"