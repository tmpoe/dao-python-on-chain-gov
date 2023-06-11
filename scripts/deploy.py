from utils import get_account
from brownie import GovernanceToken, GovernanceTimeLock, Governor, Box, config, network
from web3 import constants


MIN_DELAY = 2 * 24 * 60 * 60


def deploy_governor(redeploy=False, verify=False):
    account = get_account()

    gov_tok = (
        GovernanceToken.deploy(
            {"from": account},
            publish_source=config["networks"][network.show_active()].get(
                "verify", verify
            ),
        )
        if (redeploy or not len(GovernanceToken))
        else GovernanceToken[-1]
    )

    # is this really necessary? Why do I neet to delegate to myself?
    gov_tok.delegate(account, {"from": account})
    print(f"Checkpoints: {gov_tok.numCheckpoints(account)}")

    gov_timelock = (
        GovernanceTimeLock.deploy(
            MIN_DELAY,
            [],
            [],
            {"from": account},
            publish_source=config["networks"][network.show_active()].get(
                "verify", verify
            ),
        )
        if (redeploy or not len(GovernanceTimeLock))
        else GovernanceTimeLock[-1]
    )

    governor = (
        Governor.deploy(
            gov_tok,
            gov_timelock,
            {"from": account},
            publish_source=config["networks"][network.show_active()].get(
                "verify", verify
            ),
        )
        if (redeploy or not len(Governor))
        else Governor[-1]
    )

    proposer_role = gov_timelock.PROPOSER_ROLE()
    executor_role = gov_timelock.EXECUTOR_ROLE()
    timelock_admin_role = gov_timelock.TIMELOCK_ADMIN_ROLE()

    gov_timelock.grantRole(proposer_role, governor, {"from": account})
    gov_timelock.grantRole(executor_role, constants.ADDRESS_ZERO, {"from": account})

    # newer contract version supports admin as constructor arg
    tx = gov_timelock.revokeRole(timelock_admin_role)
    tx.wait(1)
    gov_timelock.grantRole(timelock_admin_role, account, {"from": account})


def deploy_governed_contract():
    account = get_account()
    box = Box.deploy(0, {"from": account})
    tx = box.transferOwnership(GovernanceTimeLock[-1], {"from": account})
    tx.wait(1)


def main():
    deploy_governor()
    deploy_governed_contract()
