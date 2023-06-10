from typing import Optional
from brownie import (
    network,
    accounts,
    config
)
from brownie.network.account import Account
from schemas.models import AccountImportData

NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["hardhat", "development", "ganache"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS + [
    "mainnet-fork",
    "binance-fork",
    "matic-fork",
]

def get_account(idx: Optional[int]=None, account_import_data: Optional[AccountImportData]=None) -> Account:
    if idx is not None:
        return accounts[idx]
    if id is not None:
        return accounts.load(account_import_data.file_path, account_import_data.password)
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])
    
    