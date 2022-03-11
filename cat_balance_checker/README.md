## cat-balance-checker

Parses all of your CAT's transactions from genesis to create a JSON file with balances of your CAT. Can also retrieve the XCH address in case you want to send more of the same CAT.

**Untested on multiple issuance CATs!**

```
usage: cat_balance_checker.py [-h] -t TAIL --genesis_ids GENESIS_IDS [--height HEIGHT] [--xch-address] [--hostname HOSTNAME] [-p PORT]

Get CAT balances

optional arguments:
  -h, --help            show this help message and exit
  -t TAIL, --tail TAIL  CAT tail.
  --genesis_ids GENESIS_IDS
                        Comma-separated list of coin genesis IDs
  --height HEIGHT       End height (default: latest)
  --xch-address         Try to retrieve original XCH send address
  --hostname HOSTNAME   Full node RPC hostname
  -p PORT, --port PORT  Full node RPC port
```

Sample output

```json
[
  {
    "xch19t98p4358rzkgrkuchakp50vecj94e6t4v3a3adrvtcvhdgq8yascphnw3": {
      "amount": 1.0,
      "amount_mojo": 1000,
      "xch_address": "xch1saa705v6rvf2ae887dqggxuxq35uuj7vy8a6pwnvy873tfghsqhsxqnf0c"
    }
  }
]
```
