# Variables
PYTHON := python3
VENV := venv
VENV_ACTIVATE := $(VENV)/bin/activate
PIP := $(VENV)/bin/pip
UVICORN := $(VENV)/bin/uvicorn
CELERY := $(VENV)/bin/celery
PLAYWRIGHT := $(VENV)/bin/playwright
DOCKER := docker
DOCKER_COMPOSE := docker-compose

# Docker image and container names
DOCKER_IMAGE_NAME := myapp
DOCKER_CONTAINER_NAME := myapp-container

# Phony targets
.PHONY: all setup run clean show-architecture test docker-build docker-run docker-stop docker-clean

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
	@PYTHONPATH=. $(VENV)/bin/pytest tests/

# Docker targets
docker-build:
	@echo "Building Docker image..."
	$(DOCKER) build -t $(DOCKER_IMAGE_NAME) .

docker-run: docker-build
	@echo "Running Docker container..."
	$(DOCKER) run -d --name $(DOCKER_CONTAINER_NAME) -p 8000:8000 $(DOCKER_IMAGE_NAME)

docker-stop:
	@echo "Stopping Docker container..."
	$(DOCKER) stop $(DOCKER_CONTAINER_NAME)
	$(DOCKER) rm $(DOCKER_CONTAINER_NAME)

docker-clean: docker-stop
	@echo "Removing Docker image..."
	$(DOCKER) rmi $(DOCKER_IMAGE_NAME)

# Docker Compose targets
docker-compose-up:
	@echo "Starting services with Docker Compose..."
	$(DOCKER_COMPOSE) up -d

docker-compose-down:
	@echo "Stopping services with Docker Compose..."
	$(DOCKER_COMPOSE) down

# Help target
help:
	@echo "Available commands:"
	@echo "  make setup              : Set up the virtual environment and install dependencies"
	@echo "  make run                : Start all services and run the application"
	@echo "  make clean              : Remove virtual environment and stop services"
	@echo "  make show-architecture  : Display the project architecture"
	@echo "  make test               : Run the test suite"
	@echo "  make docker-build       : Build the Docker image"
	@echo "  make docker-run         : Build and run the Docker container"
	@echo "  make docker-stop        : Stop and remove the Docker container"
	@echo "  make docker-clean       : Remove the Docker container and image"
	@echo "  make docker-compose-up  : Start services with Docker Compose"
	@echo "  make docker-compose-down: Stop services with Docker Compose"
	@echo "  make help               : Show this help message"