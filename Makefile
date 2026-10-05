PYTHON ?= python3
export PYTHONPATH := src

MAP = maps/challenger/01_the_impossible_dream.txt

install:
	$(PYTHON) -m pip install -e .

run:
	$(PYTHON) -m fly_in.cli $(MAP)

run-gui:
	$(PYTHON) -m fly_in.cli --gui $(MAP)

debug:
	$(PYTHON) -m pdb -m fly_in.cli $(MAP)

clean:
	find . -type d \( -name __pycache__ -o -name .mypy_cache -o -name .pytest_cache \) -prune -exec rm -rf {} +

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

test:
	$(PYTHON) -m unittest discover -s tests -v
