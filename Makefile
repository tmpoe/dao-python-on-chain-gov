ONESHELL:

lint:
	black .; \
	ruff --fix scripts/ tests/
