ONESHELL:

lint:
	black .; \
	ruff --fix scripts/ tests/

install:
	pip install ."[test]"