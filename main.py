from libra_client import Client
from libra_client.wallet_library import Wallet
# from libra_client.lbrtypes.bytecode import CodeType
# # from move_core_types.language_storage import core_code_address
# # from lbrtypes.account_config import association_address, transaction_fee_address
# # from banktypes.bytecode import bytecodes, CodeType

client = Client("libra_testnet")
wallet = Wallet.new()
a1 = wallet.new_account()
a2 = wallet.new_account()
client.mint_coin(a1.address, 100, auth_key_prefix=a1.auth_key_prefix)
client.transfer_coin(a1, a2.address, 10)
