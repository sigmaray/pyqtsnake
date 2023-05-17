.PHONY: snake
snake:
	python3 snake.py

.PHONY: snakeg
snakeg:
	python3 snakeg.py

.PHONY: pylint
pylint:
	pylint *.py

.PHONY: flake8
flake8:
	flake8 *.py

.PHONY: mypy
mypy:
	mypy *.py --ignore-missing-imports

.PHONY: linters
linters: flake8 pylint mypy

.PHONY: createvenv
createvenv:
	python3 -m venv .venv
	@echo "Please run << source .venv/bin/activate >> in your terminal"

.PHONY: pipinstall
pipinstall:
	pip install --upgrade pip
	pip install -r requirements.txt 

.PHONY: docker-build
docker-build:
	docker build -t pyqtsnake .

.PHONY: docker-run
docker-run:
	docker run -it -p 8080:8080 pyqtsnake

.PHONY: docker-build-and-run
docker-build-and-run:
	docker build -t pyqtsnake . && docker run -it -p 8080:8080 pyqtsnake