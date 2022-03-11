from typing import TYPE_CHECKING

import argparse
import asyncio
import logging
import os
import sys

from chia.types.blockchain_format.program import Program, INFINITE_COST
from chia.util.bech32m import encode_puzzle_hash
from chia.util.byte_types import hexstr_to_bytes
from chia.util.condition_tools import conditions_dict_for_solution
from clvm_tools.binutils import disassemble

from hbsc_utils.rpc import ChiaFullNodeWrapper

if TYPE_CHECKING:
    from chia.types.coin_spend import CoinSpend

logging.basicConfig(level=logging.INFO)


def get_announcement_value(condition):
    as_prog = Program.to(
        [condition.opcode] + [condition.vars[i] for i in range(0, len(condition.vars))]
    )
    return disassemble(as_prog)


async def process_record(record, client):
    spend: CoinSpend = await client.get_puzzle_and_solution(
        record.coin.name(), record.spent_block_index
    )
    puzzle_dis = disassemble(spend.puzzle_reveal.to_program())
    solution_dis = disassemble(spend.solution.to_program())

    print(f"{'='*73}\nCoin ID: {record.coin.name()}\n")
    print(
        f"Amount: {record.coin.amount / 1000000000000} XCH ({record.coin.amount} mojo)"
    )
    print(f"Created at height {record.confirmed_block_index}")
    print(
        f"Spent at height {record.spent_block_index} (after {record.spent_block_index - record.confirmed_block_index} blocks)"
    )
    print(f"Address: {encode_puzzle_hash(spend.puzzle_reveal.get_tree_hash(), 'xch')}")
    print(f"\nPuzzle hash: {spend.puzzle_reveal.get_tree_hash()}")
    print(puzzle_dis)
    print(f"\nSolution hash: {spend.solution.get_tree_hash()}")
    print(solution_dis)
    error, conditions, cost = conditions_dict_for_solution(
        spend.puzzle_reveal, spend.solution, INFINITE_COST
    )
    print(f"\nOutput conditions:")
    for condition_values in list(conditions.values()):
        for c in condition_values:
            print(f"{c.opcode.name}: {get_announcement_value(c)}")
    print(f"")


async def main(args):
    async with ChiaFullNodeWrapper(hostname=args.hostname, port=args.port) as (_, client):
        if args.id:
            records = [await client.get_coin_record_by_name(hexstr_to_bytes(args.id))]
        elif args.puzzle_hash:
            records = await client.get_coin_records_by_puzzle_hash(
                hexstr_to_bytes(args.puzzle_hash)
            )

        records = sorted(
            [r for r in records if r.spent], key=lambda x: x.spent_block_index
        )

        if len(records) == 0:
            print("No spent coins found.")
            sys.exit()

        for record in records:
            await process_record(record, client)


parser = argparse.ArgumentParser(description="Analyze XCH spends")
input_group = parser.add_mutually_exclusive_group()
input_group.add_argument("-id", type=str, help="Coin ID to analyze")
input_group.add_argument(
    "-ph", "--puzzle-hash", type=str, help="Coin puzzle hash to analyze"
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
