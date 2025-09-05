from typing import cast

from ape import Contract
from ape.contracts.base import ContractInstance
from eth_utils.crypto import keccak

FNS_REGISTRY = "0xd8599630DDd05aAa21Ce48F9D596AAB260352CB7"  # on Fraxtal


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
        return fns_name(address)
        # return str(networks.active_provider.web3.ens.name(address))
    except Exception:
        return address


def _namehash(name: str) -> bytes:
    node = b"\x00" * 32
    if name:
        for label in reversed(name.split(".")):
            node = keccak(node + keccak(text=label))
    return node


def fns_name(address: str) -> str:
    try:
        node = _namehash(f"{address.lower().replace('0x', '')}.addr.reverse")
        return str(Contract(Contract(FNS_REGISTRY).resolver(node)).name(node))
    except Exception:
        return address
