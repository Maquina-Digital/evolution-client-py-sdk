# --------------------------
# Python SDK Makefile
# --------------------------

# Default target
.DEFAULT_GOAL := help

# Colors for pretty output
GREEN := \033[0;32m
NC := \033[0m

# --------------------------
# Commands
# --------------------------

help:
	@echo ""
	@echo "Available commands:"
	@echo "  make install   - Install project + dev dependencies"
	@echo "  make test      - Run test suite using pytest"
	@echo "  make clean     - Clean pytest cache"
	@echo "  make reset     - Remove .venv and reinstall everything"
	@echo ""

install:
	@echo "$(GREEN)Installing dependencies...$(NC)"
	poetry install --with dev

test:
	@echo "$(GREEN)Running tests...$(NC)"
	poetry run pytest -v

clean:
	@echo "$(GREEN)Cleaning pytest cache...$(NC)"
	rm -rf .pytest_cache

reset:
	@echo "$(GREEN)Resetting environment...$(NC)"
	rm -rf .venv
	poetry install --with dev
