from violas_client import Client, Wallet
from violas_client.move_core_types.language_storage import core_code_address
from violas_client.lbrtypes.bytecode import CodeType

client = Client("bj_testnet")
for i in range(38):
    tx = client.get_account_transaction(client.BANK_OWNER_ADDRESS, i)
    print(tx.get_code_type(), tx.get_version())
# print(client.get_sequence_number(client.BANK_OWNER_ADDRESS))
# txs = client.get_transactions(957500, 1000)
# for tx in txs:
#     if tx.get_code_type() != CodeType.BLOCK_METADATA:
#         print(tx.get_amount())


# wallet = Wallet.new()
# module_account = wallet.new_account()
# client.mint_coin(module_account.address, 200_000_000, auth_key_prefix=module_account.auth_key_prefix,
#                  currency_code="USD")
# seq = client.bank_publish(module_account)
# client.get_account_transaction(module_account.address, seq).get_amount()