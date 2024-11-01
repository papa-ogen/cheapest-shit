# Makefile for the Cheapest Products project

# Variables
PYENV_VERSION = cheapest-shit
PYTHON_VERSION = 3.11.1

# Colors
GREEN = \033[0;32m
YELLOW = \033[1;33m
RED = \033[0;31m
NC = \033[0m  # No Color

# Default target
.PHONY: all install update npm-install

all:
	uvicorn app.main:app --reload & cd frontend && npm run dev

install: 
	@echo "$(YELLOW)Creating virtual environment...$(NC)"
	# pyenv virtualenv $(PYTHON_VERSION) $(PYENV_VERSION)
	# pyenv local $(PYENV_VERSION)
	@echo "$(YELLOW)Installing Python dependencies...$(NC)"
	pip install -r requirements.txt -r requirements-dev.txt
	@$(MAKE) npm-install

npm-install:
	@echo "$(GREEN)Installing npm dependencies...$(NC)"
	cd frontend && npm install

update:
	@echo "$(YELLOW)Updating dependencies...$(NC)"
	pip-compile requirements.in
	pip-compile requirements-dev.in
	pip install -r requirements.txt -r requirements-dev.txt

test:
	pytest

.PHONY: format lint isort black mypy

# Format code using isort and Black
format: isort black
	@echo "$(GREEN)Code formatted successfully with isort and Black.$(NC)"

# Run isort to organize imports
isort:
	isort app

# Run Black to format code
black:
	black app

# Run linting with Flake8
lint:
	flake8 app

# Run mypy for type checking
mypy:
	mypy app

# Run all checks (lint, type check, format)
check: lint mypy
	@echo "$(GREEN)Linting, type-checking, and formatting completed.$(NC)"