# Variables
PYTHON := python3
VENV := venv
VENV_ACTIVATE := $(VENV)/bin/activate
PIP := $(VENV)/bin/pip
UVICORN := $(VENV)/bin/uvicorn
PLAYWRIGHT := $(VENV)/bin/playwright

# Phony targets
.PHONY: all setup run clean test docker-build docker-run docker-stop docker-clean

all: setup

setup: $(VENV_ACTIVATE)
	@echo "Setup complete. Use 'make run' to start the application."

$(VENV_ACTIVATE): requirements.txt
	$(PYTHON) -m venv $(VENV)
	$(PIP) install -r requirements.txt
	$(PLAYWRIGHT) install
	@touch $(VENV_ACTIVATE)

run: setup
	@echo "Starting FastAPI application..."
	@$(UVICORN) src.main:app --reload

clean:
	@echo "Cleaning up..."
	@rm -rf $(VENV)
	@find . -type f -name '*.pyc' -delete
	@find . -type d -name '__pycache__' -delete
	@echo "Cleanup complete."

test: setup
	@echo "Running tests..."
	@PYTHONPATH=. $(VENV)/bin/pytest tests/

# Docker targets
docker-build:
	@echo "Building Docker image..."
	docker build -t product-scraper-api .

docker-run: docker-build
	@echo "Running Docker container..."
	docker run -d -p 8000:8000 --name product-scraper-api-container product-scraper-api

docker-stop:
	@echo "Stopping Docker container..."
	docker stop product-scraper-api-container
	docker rm product-scraper-api-container

docker-clean: docker-stop
	@echo "Removing Docker image..."
	docker rmi product-scraper-api

# Help target
help:
	@echo "Available commands:"
	@echo "  make setup              : Set up the virtual environment and install dependencies"
	@echo "  make run                : Start the FastAPI application"
	@echo "  make clean              : Remove virtual environment and cached files"
	@echo "  make test               : Run the test suite"
	@echo "  make docker-build       : Build the Docker image"
	@echo "  make docker-run         : Build and run the Docker container"
	@echo "  make docker-stop        : Stop and remove the Docker container"
	@echo "  make docker-clean       : Remove the Docker container and image"
	@echo "  make help               : Show this help message"