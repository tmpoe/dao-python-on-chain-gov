from brownie import Contract, Box, MyGovernor
from web3 import Web3

from scripts.utils import get_account

PROPOSAL_DESCRIPTION = "Change box value"


def propose(box, new_value_to_store):
    account = get_account()

    encoded_box_store_func = Contract.from_abi("Box", box, Box.abi).store.encode_input(
        new_value_to_store
    )

    proposal_tx = MyGovernor[-1].propose(
        [box.address],
        [0],
        [encoded_box_store_func],
        PROPOSAL_DESCRIPTION,
        {"from": account},
    )
    proposal_tx.wait(1)

    return proposal_tx.events["ProposalCreated"]["proposalId"]


def vote(proposal_id: int, vote: int):
    # 0 = Against, 1 = For, 2 = Abstain
    account = get_account()
    tx = MyGovernor[-1].castVoteWithReason(
        proposal_id, vote, "Want it changed", {"from": account}
    )
    tx.wait(1)


def queue(store_value):
    account = get_account()

    tx = MyGovernor[-1].queue(
        [Box[-1].address],
        [0],
        [_get_encoded_function(store_value)],
        Web3.keccak(text=PROPOSAL_DESCRIPTION).hex(),
        {"from": account},
    )
    tx.wait(1)


def execute(store_value):
    account = get_account()
    tx = MyGovernor[-1].execute(
        [Box[-1].address],
        [0],
        [_get_encoded_function(store_value)],
        Web3.keccak(text=PROPOSAL_DESCRIPTION).hex(),
        {"from": account},
    )
    tx.wait(1)


def _get_encoded_function(store_value):
    args = (store_value,)
    return Contract.from_abi("Box", Box[-1], Box.abi).store.encode_input(*args)
