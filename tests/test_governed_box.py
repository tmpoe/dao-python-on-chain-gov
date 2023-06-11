from time import sleep
from brownie import Box, MyGovernor
from scripts.config import DeployConfig

from scripts.deploy import deploy_governed_box
from scripts.governance import propose, queue, execute, vote

TEST_BOX_VALUE = 42


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
    WHEN: Proposal is called on box to change its stored value to TEST_BOX_VALUE
    THEN: The proposal is created and the stored value is not changed
    """
    deploy_governed_box(TestDeployConfig())
    box = Box[-1]

    proposal_id = propose(box, TEST_BOX_VALUE)
    assert proposal_id
    assert box.retrieve() == 0
    assert MyGovernor[-1].state(proposal_id) == 0  # pending
    assert MyGovernor[-1].proposalDeadline(proposal_id)
    assert MyGovernor[-1].proposalSnapshot(proposal_id)


def test_governable_box_proposal_executed(move_blocks):
    """
    GIVEN: A succesful proposal
    WHEN: Proposal is executed
    THEN: The stored value is changed to TEST_BOX_VALUE
    """
    config = TestDeployConfig()
    deploy_governed_box(config)
    box = Box[-1]

    proposal_id = propose(box, TEST_BOX_VALUE)
    
    move_blocks(2)
    vote(proposal_id, 1)
    move_blocks(config.VOTING_PERIOD)
    
    queue(TEST_BOX_VALUE)
    sleep(config.MIN_DELAY)
    execute(TEST_BOX_VALUE)
    
    assert box.retrieve() == TEST_BOX_VALUE
