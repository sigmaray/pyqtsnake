.PHONY: snake
snake:
	python3 snake.py

.PHONY: snakeg
snakeg:
	python3 snakeg.py

.PHONY: pylint
pylint:
	pylint *.py

.PHONY: mypy
mypy:
	mypy *.py --ignore-missing-imports
