VERSION=0.`git rev-list --count HEAD`
.PHONY: black

DOCKER_BUILD=docker build

ifeq ($(shell uname -m), arm64)
DOCKER_BUILD=docker buildx build --platform linux/amd64
endif

build:
	$(DOCKER_BUILD) -t registry.domandoman.xyz/fooder/api -f Dockerfile .

push:
	docker push registry.domandoman.xyz/fooder/api

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
