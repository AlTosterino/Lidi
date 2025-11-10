PROJECT_PATH = $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
SRC_PATH = src
TESTS_PATH = tests
LINT_PATHS = \
$(SRC_PATH) \
$(TESTS_PATH)

sync-deps:
	uv sync

update-deps:
	uv lock --upgrade

lint:
	uv run black $(LINT_PATHS)
	uv run ruff check $(LINT_PATHS) --fix
	uv run mypy $(LINT_PATHS)

lint-ci:
	uv run black --check $(LINT_PATHS)
	uv run ruff check $(LINT_PATHS)
	uv run mypy $(LINT_PATHS)

test:
	uv run pytest

test-ci:
	uv run coverage run -m --source=lidipy pytest