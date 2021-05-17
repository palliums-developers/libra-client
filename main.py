import random
import time
from libra_client import Client, Wallet

from violas_client import Wallet, Client
from violas_client.move_core_types.language_storage import core_code_address

client = Client("bj_testnet")
wallet = Wallet.new()
liquidity_account = wallet.new_account()
client.mint_coin(liquidity_account.address, 10_000_000, auth_key_prefix=liquidity_account.auth_key_prefix,
                 is_blocking=True, currency_code="vUSDT")
client.add_currency_to_account(liquidity_account, "vBTC")
client.mint_coin(liquidity_account.address, 10_000_000, currency_code="vBTC",
                 auth_key_prefix=liquidity_account.auth_key_prefix, is_blocking=True)
