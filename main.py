from violas_client.client import Client
from lbrtypes.bytecode import CodeType

client = Client("bj_testnet")
txs = client.get_transactions(257000, 1000)

# for tx in txs:
#     if tx.get_code_type() != CodeType.BLOCK_METADATA:
#         print()