from typing import cast

from ape import Contract, networks
from ape.contracts.base import ContractInstance


def auction_house() -> ContractInstance:
    return cast(ContractInstance, Contract("0xd184CF2f60Da3C54eD1fc371a3e04179C41570c6"))


def squid() -> ContractInstance:
    return cast(ContractInstance, Contract("0x6e58089d8E8f664823d26454f49A5A0f2fF697Fe"))


def explorer_address_url() -> str:
    return "https://fraxscan.com/address/"


def explorer_tx_url() -> str:
    return "https://fraxscan.com/tx/"


def ens_name(address: str) -> str:
    try:
        return str(networks.active_provider.web3.ens.name(address))
    except Exception:
        return address
