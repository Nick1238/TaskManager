VENV_NAME = venv
PYTHON = python3
PIP = $(VENV_NAME)/bin/pip
PYTEST = $(VENV_NAME)/bin/pytest
ACTIVATE_VENV = . $(VENV_NAME)/bin/activate 

.PHONY: all install test clean lint run

all: install test

install:
	$(PYTHON) -m venv $(VENV_NAME)
	. $(VENV_NAME)/bin/activate && $(PIP) install -r requirements.txt

test:
	. $(VENV_NAME)/bin/activate && $(PYTEST)

clean:
	rm -rf $(VENV_NAME)
	rm -rf .pytest_cache

lint:
	. $(VENV_NAME)/bin/activate
	isort src/
	ruff check src/

run:
	. $(VENV_NAME)/bin/activate && $(PYTHON) src/main.py
