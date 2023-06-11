from brownie import Box, MyGovernor
from scripts.config import DeployConfig

from scripts.deploy import deploy_governed_box
from scripts.governance import propose


class TestDeployConfig(DeployConfig):
    VOTING_PERIOD = 5  # blocks
    VOTING_DELAY = 1  # block
    MIN_DELAY = 1  # sec
    QUORUM_FRACTION = 1


def test_governable_box_deploy():
    """
    GIVEN: N/A
    WHEN: Governed box is deployed with depenencies
    THEN: The governor's timelock is the owner of the box
    """
    deploy_governed_box(TestDeployConfig())
    assert Box[-1].owner() == MyGovernor[-1].timelock()


def test_governable_box_proposal_can_be_initiated():
    """
    GIVEN: A box
    WHEN: Proposal is called on box to change its stored value to 42
    THEN: The proposal is created and the stored value is not changed
    """
    deploy_governed_box(TestDeployConfig())
    box = Box[-1]

    proposal_id = propose(box, 42)
    assert proposal_id
    assert box.retrieve() == 0
    assert MyGovernor[-1].state(proposal_id) == 0  # pending
    assert MyGovernor[-1].proposalDeadline(proposal_id)
    assert MyGovernor[-1].proposalSnapshot(proposal_id)


def test_governable_box_voting(monkeypatch):
    """
    GIVEN: A box
    WHEN: Proposal is called on box to change its stored value to 42
    THEN: The proposal is created and the stored value is not changed
    """
    deploy_governed_box(TestDeployConfig())
    box = Box[-1]

    proposal_id = propose(box, 42)
    assert proposal_id
    assert box.retrieve() == 0
    assert MyGovernor[-1].state(proposal_id) == 0  # pending
    assert MyGovernor[-1].proposalDeadline(proposal_id)
    assert MyGovernor[-1].proposalSnapshot(proposal_id)
