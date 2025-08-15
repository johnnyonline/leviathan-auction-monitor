from typing import Any, Dict, Optional

import requests
from ape import networks

from bot.config import auction_house


def _leviathan_base_url() -> str:
    chain_id = networks.active_provider.chain_id
    house = auction_house().address
    return f"https://api.leviathannews.xyz/api/v1/auction_contract/{chain_id}/{house}/"


def _parse_auction(obj: Dict[str, Any]) -> Dict[str, Any]:
    meta = obj.get("metadata") or {}
    attrs = {a.get("trait_type"): a.get("value") for a in meta.get("attributes", []) if isinstance(a, dict)}
    return {
        "auction_id": obj.get("auction_id"),
        "chain_id": obj.get("chain_id"),
        "contract_address": obj.get("contract_addr"),
        "name": meta.get("name"),
        "description": meta.get("description"),
        "image_url": meta.get("image_url"),
        "attributes": attrs,
        "created_at": obj.get("created_at"),
        "updated_at": obj.get("updated_at"),
        "ipfs_hash": obj.get("ipfs_hash"),
        "ipfs_status": obj.get("ipfs_status"),
    }


def auction_data(auction_id: Optional[int] = None) -> Dict[str, Any]:
    base = _leviathan_base_url()
    url = f"{base}{auction_id}/" if auction_id is not None else base

    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as e:
        print(f"[fetch_leviathan_auctions] HTTP error: {e}")
        return {}
    except ValueError as e:
        print(f"[fetch_leviathan_auctions] JSON decode error: {e}")
        return {}

    if auction_id is not None:
        return _parse_auction(data)

    results = data.get("results", [])
    return {
        "total_auctions": data.get("count"),
        "current_page": data.get("current_page"),
        "total_pages": data.get("total_pages"),
        "results": [_parse_auction(a) for a in results if isinstance(a, dict)],
    }
