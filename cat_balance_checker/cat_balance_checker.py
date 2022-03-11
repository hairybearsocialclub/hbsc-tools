from typing import Dict, List, Optional, TypedDict

import argparse
import asyncio
import json
import logging
import os

from chia.types.blockchain_format.coin import Coin

from chia.types.coin_record import CoinRecord
from chia.util.byte_types import hexstr_to_bytes
from chia.util.bech32m import encode_puzzle_hash

from hbsc_utils.rpc import ChiaFullNodeWrapper
from hbsc_utils.spends import extract_payments_from_spend


class AddressData(TypedDict):
    balance: float
    balance_mojo: int
    xch_address: Optional[str]


AddressBalanceDict = Dict[str, AddressData]
balances: AddressBalanceDict = {}

logging.basicConfig(level=logging.INFO)


def save_results(results: AddressBalanceDict, tail: str, height: int):
    with open(f"balances-{tail[:6]}-{height}.json", "w") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


# traverse the tree until only unspent coins are left
async def traverse(
    record: CoinRecord,
    wrapper: ChiaFullNodeWrapper,
    end_height: int,
    tail: str,
    want_xch_address: bool = False,
):
    coin = record.coin
    client = wrapper._client
    if not record.spent or (record.spent and record.spent_block_index > end_height):
        logging.info(f"Found unspent coin: {record.coin.puzzle_hash}")
        cat_address = encode_puzzle_hash(coin.puzzle_hash, "xch")
        amount = coin.amount / float(1000)
        if cat_address in balances:
            balances[cat_address]["balance"] += amount
            balances[cat_address]["balance_mojo"] += coin.amount
        else:
            balances[cat_address] = {"balance": amount, "balance_mojo": coin.amount}

        if want_xch_address:
            try:
                xch_address = await wrapper.get_original_address_for_cat(record, tail)
            except:
                logging.warning(f"Failed to get XCH address for {cat_address}")
                xch_address = None
            balances[cat_address]["xch_address"] = xch_address
    else:
        created_coins: List[CoinRecord] = []

        # retrieve coin spend and payments
        spend = await client.get_puzzle_and_solution(
            record.name, record.spent_block_index
        )
        payments = extract_payments_from_spend(spend)

        for p in payments:
            c = Coin(
                parent_coin_info=record.name, puzzle_hash=p.puzzle_hash, amount=p.amount
            )
            r = await client.get_coin_record_by_name(c.name())
            created_coins.append(r)

        logging.debug(
            f"Found created coins: {', '.join([record.coin.name().__str__() for record in created_coins])}"
        )
        for r in created_coins:
            await traverse(r, wrapper, end_height, tail, want_xch_address)


async def main(args):
    async with ChiaFullNodeWrapper(hostname=args.hostname, port=args.port) as (
        wrapper,
        client,
    ):
        if args.height is None:
            state = await client.get_blockchain_state()
            args.height = state["peak"].height
        logging.info(f"Using height {args.height}")

        for coin_id in args.genesis_ids.split(","):
            initial_record = await client.get_coin_record_by_name(
                hexstr_to_bytes(coin_id.strip())
            )
            await traverse(
                initial_record, wrapper, args.height, args.tail, args.xch_address
            )

    balances_sorted = dict(
        sorted(balances.items(), key=lambda i: i[1]["balance"], reverse=True)
    )
    save_results(balances_sorted, args.tail, args.height)


parser = argparse.ArgumentParser(description="Get CAT balances")
parser.add_argument(
    "-t",
    "--tail",
    type=str,
    required=True,
    help=f"CAT tail.",
)
parser.add_argument(
    "--genesis_ids",
    type=str,
    required=True,
    help="Comma-separated list of coin genesis IDs",
)
parser.add_argument("--height", type=int, help="End height (default: latest)")
parser.add_argument(
    "--xch-address",
    action="store_true",
    help="Try to retrieve original XCH send address",
)
parser.add_argument(
    "--hostname",
    type=str,
    default=os.getenv("CHIA_FULL_NODE_HOSTNAME", "127.0.0.1"),
    help="Full node RPC hostname",
)
parser.add_argument(
    "-p",
    "--port",
    type=int,
    default=int(os.getenv("CHIA_FULL_NODE_PORT", "8555")),
    help="Full node RPC port",
)
args = parser.parse_args()
asyncio.run(main(args))
