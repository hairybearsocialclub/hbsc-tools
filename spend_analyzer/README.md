## spend-analyzer
Allows you to analyze Chia coin spends.

```
usage: spend_analyzer.py [-h] [-id ID | -ph PUZZLE_HASH] [--hostname HOSTNAME] [-p PORT]

Analyze XCH spends

optional arguments:
  -h, --help            show this help message and exit
  -id ID                Coin ID to analyze
  -ph PUZZLE_HASH, --puzzle-hash PUZZLE_HASH
                        Coin puzzle hash to analyze
  --hostname HOSTNAME   Full node RPC hostname
  -p PORT, --port PORT  Full node RPC port
```

Sample output:
```
❯ python spend_analyzer.py -id 0xdce550a4341e5ec31c7e3fe5c6ab9801c66ed02689725939537d8d4492465800
=========================================================================
Coin ID: dce550a4341e5ec31c7e3fe5c6ab9801c66ed02689725939537d8d4492465800

Amount: 2625000.0 XCH (2625000000000000000 mojo)
Created at height 1
Spent at height 228799 (after 228798 blocks)
Address: xch18krkt5a9jlkpmxtx8akfs9kezkuldpsn4j2qpxyycjka4m7vu6hstf6hku

Puzzle hash: 3d8765d3a597ec1d99663f6c9816d915b9f68613ac94009884c4addaefcce6af
(q (51 0x1b7ab2079fa635554ad9bd4812c622e46ee3b1875a7813afba127bb0cc9794f9 0x1236efcbcbb34000) (51 0x6f184a7074c925ef8688ce56941eb8929be320265f824ec7e351356cc745d38a 0x1236efcbcbb34000))

Solution hash: 4bf5122f344554c53bde2ebb8cd2b7e3d1600ad631c385a5d7cce23c7785459a
()

Output conditions:
CREATE_COIN: (51 0x1b7ab2079fa635554ad9bd4812c622e46ee3b1875a7813afba127bb0cc9794f9 0x1236efcbcbb34000)
CREATE_COIN: (51 0x6f184a7074c925ef8688ce56941eb8929be320265f824ec7e351356cc745d38a 0x1236efcbcbb34000)
```
