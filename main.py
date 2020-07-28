from libra_client import Client
from libra_client.wallet_library import Wallet
from libra_client.lbrtypes.bytecode import CodeType
# from move_core_types.language_storage import core_code_address
# from lbrtypes.account_config import association_address, transaction_fee_address
# from banktypes.bytecode import bytecodes, CodeType

client = Client("libra_testnet")
wallet = Wallet.new()
a1 = wallet.new_account()
client.mint_coin(a1.address_hex, 22, auth_key_prefix=a1.auth_key_prefix, currency_code="Coin1")
print(client.get_balances(a1.address_hex))
start = 0
while True:
    txs = client.get_transactions(start, 500, True)
    for tx in txs:
        if tx.get_code_type() != CodeType.BLOCK_METADATA:
            print(tx)
    start += 500
    print(start)

# balances = client.get_balances(a1.address_hex)
# assert balances["LBR"] == 11
# assert balances["Coin1"] == 22