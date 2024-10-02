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

# Phony targets
.PHONY: all setup run clean

# Default target
all: setup run

# Setup virtual environment and install dependencies
setup:
	@echo "Setting up virtual environment..."
	@$(PYTHON) -m venv $(VENV)
	@$(VENV_ACTIVATE) && pip install -r requirements.txt

# Run the script
run:
	@echo "Running the script..."
	@$(VENV_ACTIVATE) && $(PYTHON) $(SCRIPT)

# Clean up
clean:
	@echo "Cleaning up..."
	@rm -rf $(VENV)
	@rm -f $(OUTPUT)

# Show help
help:
	@echo "Available targets:"
	@echo "  setup  : Set up virtual environment and install dependencies"
	@echo "  run    : Run the script"
	@echo "  clean  : Remove virtual environment and output file"
	@echo "  all    : Setup and run (default)"
	@echo "  help   : Show this help message"