import pytest
from brownie import chain

from scripts.utils import get_account


@pytest.fixture
def move_blocks():
    def _inner(amount):
        for block in range(amount):
            get_account().transfer(get_account(), "0 ether")
        print(f"Moved {amount} blocks. Chaint at {chain.height}")

    return _inner
