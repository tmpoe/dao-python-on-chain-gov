ONESHELL:

test:
	set -o allexport; source .env; set +o allexport; brownie test

lint:
	black .; \
	ruff --fix scripts/ tests/

install:
	pip install ."[test]"