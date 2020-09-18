from violas_client import Client, Wallet
from violas_client.move_core_types.language_storage import core_code_address
from violas_client.lbrtypes.bytecode import CodeType

client = Client("bj_testnet")
tx =client.get_transaction(957847)
print(tx.get_code_type(), tx.get_price())
# print(client.get_sequence_number(client.BANK_OWNER_ADDRESS))
# txs = client.get_transactions(957500, 1000)
# for tx in txs:
#     if tx.get_code_type() != CodeType.BLOCK_METADATA:
#         print(tx.get_amount())