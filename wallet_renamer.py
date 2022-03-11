from typing import List, Tuple

import argparse
import asyncio
import json
import logging
import re
import sys

from hbsc_utils.rpc import ChiaWalletWrapper

logging.basicConfig(level=logging.INFO)

with open("cats.json", "r") as f:
    cats = json.load(f)


async def main(args):
    async with ChiaWalletWrapper(hostname=args.hostname, port=args.port) as (_, client):
        renames: List[Tuple[int, str]] = []
        unknown_tails: List[str] = []

        wallet_fingerprint = await client.get_logged_in_fingerprint()
        logging.info(f"Connected to wallet with fingerprint {wallet_fingerprint}")
        wallets = [w for w in await client.get_wallets() if w["id"] != 1 and w["name"].upper() != "POOL WALLET"]

        for w in wallets:
            if re.search(r"CAT\s[a-z0-9]+", w["name"]) or args.force:
                if (tail := w["data"]) in cats or (tail := w["data"][:-2]) in cats:
                    name = f"{cats[tail]['name']} ({cats[tail]['ticker']})"
                    logging.info(f"Found CAT {name} ({tail})")
                    renames.append((w["id"], name))
                    await client.set_cat_name(w["id"], name)
                else:
                    logging.warning(f"Unknown CAT: {w['name']} ({w['data']})")
                    unknown_tails.append(w["data"])

        print()
        if len(renames) == 0:
            print(f"No wallets found to rename ({len(unknown_tails)} unknown).")
            sys.exit()

        print(f"Will rename {len(renames)} CATs.")
        if (answer := input(r"Proceed? (y\n) > ").strip().lower()) == "y" or answer == "yes":
            for wallet_id, name in renames:
                await c.set_cat_name(wallet_id, name)
            print("Renaming complete. Log in and out of your wallet to see changes.")
        else:
            sys.exit()


parser = argparse.ArgumentParser(description="Auto-rename CATs in Chia wallet")
parser.add_argument(
    "-i",
    "--input-file",
    type=str,
    default="cats.json",
    help=r"JSON file containing CAT data with format [{tail: {name: 'NAME', ticker: 'TKR'}}, ...]",
)
parser.add_argument(
    "--hostname", type=str, default="127.0.0.1", help="Wallet RPC hostname"
)
parser.add_argument("-p", "--port", type=int, default=9256, help="Wallet RPC port")
parser.add_argument("-f", "--force", action="store_true", help="Force rename known CATs")
args = parser.parse_args()
asyncio.run(main(args))
