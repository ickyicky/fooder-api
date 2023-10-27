VERSION=0.`git rev-list --count HEAD`
.PHONY: black


black:
	black .

.PHONY: mypy
mypy:
	mypy .

.PHONY: flake
flake:
	flake8 .

.PHONY: lint
lint: black mypy flake

.PHONY: version
version:
	@echo $(VERSION)

.PHONY: create-venv
create-venv:
	python3 -m venv .venv --prompt="fooderapi-venv" --system-site-packages
	bash -c "source .venv/bin/activate && pip install -r requirements_local.txt"

.PHONY: test
test:
	./test.sh
