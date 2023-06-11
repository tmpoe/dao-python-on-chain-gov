from scripts.config import DeployConfig
from scripts.utils import get_account
from brownie import (
    GovernanceToken,
    GovernanceTimelock,
    MyGovernor,
    Box,
    config,
    network,
)
from web3 import constants


def deploy_governor(account, deployConfig: DeployConfig, redeploy=False, verify=False):

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
    # it is - you always have to delegate the voting power of the token
    # at mint none is delegated
    # usually at transfer it is autodelegated to the trasnferee
    gov_tok.delegate(account, {"from": account})

    gov_timelock = (
        GovernanceTimelock.deploy(
            deployConfig.MIN_DELAY,
            [],
            [],
            {"from": account},
            publish_source=config["networks"][network.show_active()].get(
                "verify", verify
            ),
        )
        if (redeploy or not len(GovernanceTimelock))
        else GovernanceTimelock[-1]
    )

    governor = (
        MyGovernor.deploy(
            gov_tok,
            gov_timelock,
            deployConfig.QUORUM_FRACTION,
            deployConfig.VOTING_PERIOD,
            deployConfig.VOTING_DELAY,
            {"from": account},
            publish_source=config["networks"][network.show_active()].get(
                "verify", verify
            ),
        )
        if (redeploy or not len(MyGovernor))
        else MyGovernor[-1]
    )

    proposer_role = gov_timelock.PROPOSER_ROLE()
    executor_role = gov_timelock.EXECUTOR_ROLE()

    gov_timelock.grantRole(proposer_role, governor, {"from": account})
    gov_timelock.grantRole(executor_role, constants.ADDRESS_ZERO, {"from": account})


def deploy_governed_box(deployConfig: DeployConfig):
    account = get_account()
    deploy_governor(account, deployConfig)
    box = deploy_box(account)
    tx = box.transferOwnership(GovernanceTimelock[-1], {"from": account})
    tx.wait(1)


def deploy_box(account):
    return Box.deploy({"from": account})


def main():
    deploy_governed_box()
