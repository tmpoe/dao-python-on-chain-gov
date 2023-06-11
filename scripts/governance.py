from brownie import Contract, Box, MyGovernor

from scripts.utils import get_account


def propose(box, new_value_to_store):
    account = get_account()

    encoded_box_store_func = Contract.from_abi("Box", box, Box.abi).store.encode_input(
        new_value_to_store
    )

    proposal_tx = MyGovernor[-1].propose(
        [box.address],
        [0],
        [encoded_box_store_func],
        "Change box value",
        {"from": account},
    )
    proposal_tx.wait(1)

    return proposal_tx.events["ProposalCreated"]["proposalId"]
