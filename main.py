from libra_client import Client
from libra_client.wallet_library import Wallet
# from move_core_types.language_storage import core_code_address
# from lbrtypes.account_config import association_address, transaction_fee_address
# from banktypes.bytecode import bytecodes, CodeType

client = Client("libra_testnet")
wallet = Wallet.new()
a1 = wallet.new_account()
client.mint_coin(a1.address_hex, 22, auth_key_prefix=a1.auth_key_prefix, currency_code="Coin1")
# balances = client.get_balances(a1.address_hex)
# assert balances["LBR"] == 11
# assert balances["Coin1"] == 22