from violas_client import Client, Wallet
from violas_client.lbrtypes.account_config.constants.addresses import transaction_fee_address, testnet_dd_account_address, association_address
from violas_client.move_core_types.language_storage import CORE_CODE_ADDRESS
# # from libra_client.wallet_library import Wallet
import json

client = Client("violas_testnet")
print(client.get_transaction(13827863))

# client = Client("bj_testnet")
# client.set_exchange_module_address(association_address())
# client.set_exchange_owner_address(CORE_CODE_ADDRESS)
# wallet = Wallet.new()
# liquidity_account = wallet.new_account()
# client.mint_coin(liquidity_account.address, 10_000_000, auth_key_prefix=liquidity_account.auth_key_prefix,
#                  is_blocking=True)
# client.add_currency_to_account(liquidity_account, "Coin1")
# client.mint_coin(liquidity_account.address, 10_000_000, currency_code="Coin1",
#                  auth_key_prefix=liquidity_account.auth_key_prefix, is_blocking=True)
#
# swap_account = wallet.new_account()
# client.mint_coin(swap_account.address, 10_000_000, auth_key_prefix=swap_account.auth_key_prefix, is_blocking=True)
# client.add_currency_to_account(swap_account, "Coin1")
# client.mint_coin(swap_account.address, 10_000_000, currency_code="Coin1", auth_key_prefix=swap_account.auth_key_prefix,
#                  is_blocking=True)
#
# lbr_before_balance = client.get_balance(liquidity_account.address, "LBR")
# coin1_before_balance = client.get_balance(liquidity_account.address, "Coin1")
# client.swap_add_liquidity(liquidity_account, "LBR", "Coin1", 1_000_000, 321_432)
#

