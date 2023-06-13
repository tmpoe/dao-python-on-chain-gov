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

add-sepolia:
	set -o allexport; source .env; brownie networks add Ethereum sepolia host="https://sepolia.infura.io/v3/${WEB3_INFURA_PROJECT_ID}" chainid=11155111

deploy-sepolia:
	set -o allexport; source .env; brownie run scripts/deploy.py --network sepolia