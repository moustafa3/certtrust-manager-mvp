.PHONY: run test lint format check

run:
	uvicorn app.main:app --reload

test:
	pytest

lint:
	ruff check .

format:
	ruff format .

check:
	ruff check .
	pytest