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
brownie compile
```

Run tests

```
set -o allexport; source .env; set +o allexport; brownie test (--trace)
```
