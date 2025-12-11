from typing import cast

from ape import Contract, networks
from ape.contracts.base import ContractInstance


def auction_house() -> ContractInstance:
    return cast(ContractInstance, Contract("0xfF737F349e40418Abd9D7b3c865683f93cA3c890"))


def explorer_address_url() -> str:
    return "https://etherscan.io/address/"


def explorer_tx_url() -> str:
    return "https://etherscan.io/tx/"


def ens_name(address: str) -> str:
    try:
        ens_name = networks.active_provider.web3.ens.name(address)
        if ens_name is None:
            return str(address)
        return str(ens_name)
    except Exception:
        return str(address)
