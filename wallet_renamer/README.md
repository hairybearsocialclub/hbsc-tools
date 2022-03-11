# wallet-renamer

Allows you to auto-rename CATs in your wallet. Currently based on an offline DB parsed from taildatabase, will have to find a way to update it for everyone.

## Usage

```
usage: wallet_renamer.py [-h] [-i INPUT_FILE] [--hostname HOSTNAME] [-p PORT] [-f]

Auto-rename CATs in Chia wallet

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FILE, --input-file INPUT_FILE
                        JSON file containing CAT data with format [{tail: {name: 'NAME', ticker: 'TKR'}}, ...]
  --hostname HOSTNAME   Wallet RPC hostname
  -p PORT, --port PORT  Wallet RPC port
  -f, --force           Force rename known CATs
```

Sample output:

```
❯ python wallet_renamer.py
INFO:root:Connected to wallet with fingerprint 123123123
INFO:root:Found CAT MojoWhale (MJW) (7f3584af7b574030af5be244b6ae332fd3820b44e96e4880bbe7aa8cc05edc88)

Will rename 1 CATs.
Proceed? (y\n) > y
Renaming complete. Log in and out of your wallet to see changes.
```