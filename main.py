from violas_client import Client, Wallet
from violas_client.lbrtypes.account_config.constants.addresses import transaction_fee_address
# from libra_client.wallet_library import Wallet

client = Client("bj_testnet")
wallet = Wallet.new()
a1 = wallet.new_account()
a2 = wallet.new_account()
client.mint_coin(a1.address, 1000000, auth_key_prefix=a1.auth_key_prefix, is_blocking=True, currency_code="USD")
client.mint_coin(a2.address, 1000000, auth_key_prefix=a1.auth_key_prefix, is_blocking=True, currency_code="USD")
seq = client.transfer_coin(a1, a2.address, 100, gas_unit_price=1, currency_code="USD", gas_currency_code="USD")

