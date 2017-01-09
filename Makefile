.PHONY: all clean check wheel sdist

ifeq ($(OS),Windows_NT)
EXE=.exe
else
EXE=
endif

BUILDOUT=bin/buildout$(EXE)

all: check wheel

clean:
	rm -rf *.pyc *~ bin build dist develop-eggs .eggs eggs parts .installed.cfg *.egg-info

$(BUILDOUT):
	python bootstrap-buildout.py

eggs/%.egg bin/%$(EXE): $(BUILDOUT)
	bin/buildout -qqq

wheel: eggs/wheel*.egg $(BUILDOUT)
	bin/py setup.py bdist_wheel

sdist: $(BUILDOUT)
	bin/py setup.py sdist

check: bin/flake8$(EXE)
	bin/flake8 src
