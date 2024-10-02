# Variables
PYTHON := python3
VENV := venv
VENV_ACTIVATE := $(VENV)/bin/activate
PIP := $(VENV)/bin/pip
UVICORN := $(VENV)/bin/uvicorn
CELERY := $(VENV)/bin/celery
PLAYWRIGHT := $(VENV)/bin/playwright

# Phony targets
.PHONY: all setup run clean show-architecture test

all: setup

setup: $(VENV_ACTIVATE)
	@echo "Setup complete. Use 'make run' to start the application."

$(VENV_ACTIVATE): requirements.txt
	$(PYTHON) -m venv $(VENV)
	$(PIP) install -r requirements.txt
	$(PLAYWRIGHT) install
	@touch $(VENV_ACTIVATE)

run: setup
	@echo "Starting Redis..."
	@if ! redis-server --daemonize yes; then \
		echo "Failed to start Redis. Please make sure Redis is installed and try again."; \
		exit 1; \
	fi
	@echo "Starting Celery worker..."
	@echo "Starting FastAPI application..."
	@$(UVICORN) main:app --reload

clean:
	@echo "Cleaning up..."
	@rm -rf $(VENV)
	@find . -type f -name '*.pyc' -delete
	@find . -type d -name '__pycache__' -delete
	@echo "Stopping Redis..."
	@redis-cli shutdown
	@echo "Cleanup complete."

show-architecture:
	@cat architecture.txt

test: setup
	@echo "Running tests..."
	@$(VENV)/bin/pytest

# Help target
help:
	@echo "Available commands:"
	@echo "  make setup              : Set up the virtual environment and install dependencies"
	@echo "  make run                : Start all services and run the application"
	@echo "  make clean              : Remove virtual environment and stop services"
	@echo "  make show-architecture  : Display the project architecture"
	@echo "  make test               : Run the test suite"
	@echo "  make help               : Show this help message"