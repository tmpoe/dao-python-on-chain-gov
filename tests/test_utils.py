import json
import os
from brownie.network.account import Account
from brownie import web3
from schemas.models import AccountImportData

from scripts.utils import get_account


def test_get_account_by_index():
    """
    GIVEN: An index for an account the get
    WHEN get_account is called with the index
    THEN A non-zero account is returned
    """
    idx = 0
    account = get_account(idx=idx)
    assert account
    assert isinstance(account, Account)


def test_get_account_by_id():
    """
    GIVEN: An id for an account the get
    WHEN get_account is called with the id
    THEN A non-zero account is returned
    """
    random_private_key = os.environ.get("RANDOM_PRIVATE_KEY")
    random_mnemonic = os.environ.get("RANDOM_MNEMONIC")
    acc_data = web3.eth.account.encrypt(random_private_key, random_mnemonic)
    file_path = os.path.join(os.getcwd(), "acc.json")

    with open(file_path, "w") as outfile:
        json.dump(json.dumps(acc_data), outfile)

    account = get_account(
        account_import_data=AccountImportData(
            file_path=file_path, password=random_mnemonic
        )
    )

    os.remove(file_path)

    assert account.address[2:].lower() == acc_data["address"]
