.PHONY: all clean check wheel sdist

ifeq ($(OS),Windows_NT)
BIN=./venv/Scripts
else
BIN=./venv/bin
endif

PIP=$(BIN)/pip
PYTHON=$(BIN)/python
PIPINSTALL=$(PIP) install -q
SETUP.PY=$(BIN)/python setup.py -q
FLAKE8=$(BIN)/flake8

all: check wheel

clean:
	rm -rf *.pyc *~ bin build dist *.egg-info venv

venv:
	virtualenv -q venv
	$(PIPINSTALL) flake8 
	$(PIPINSTALL) -r requirements.txt
	$(PIPINSTALL) -e .

wheel: venv
	$(SETUP.PY) bdist_wheel

sdist: venv
	$(SETUP.PY) sdist

check: venv
	$(FLAKE8) globcopy
