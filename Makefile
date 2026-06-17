.PHONY: help install test clean status

help:
	@echo "Available commands:"
	@echo "  make install   Install package in editable mode"
	@echo "  make test      Run tests"
	@echo "  make clean     Remove cache files"
	@echo "  make status    Show git status"

install:
	pip install -e .

test:
	pytest -q

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type d -name ".ipynb_checkpoints" -prune -exec rm -rf {} +

status:
	git status --short
