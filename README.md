# Basic DAO in Python

The basis of this repo is the 2021 Chainlink hackathon found here https://www.youtube.com/watch?v=rD8AxZ_wBA4

We'll see where else I can go with this. Maybe will create a new repo after having enough fun with this and my own DAO from scratch.

Install

```
brownie - https://pypi.org/project/eth-brownie/

yarn install

pip install -c constraints.txt .
```

Compile

```
make compile
```

Run tests

```
make test
```

Lint

```
make lint
```

Add sepolia

```
brownie networks add Ethereum sepolia host="https://rpc.sepolia.dev" chainid=11155111
```
