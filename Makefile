ONESHELL:

test:
	set -o allexport; source .env; set +o allexport; brownie test

echo-test:
	echo "set -o allexport; source .env; set +o allexport; brownie test"

lint:
	black .; \
	ruff scripts/ tests/

install:
	pip install ."[test]"

compile:
	brownie compile