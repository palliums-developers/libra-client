import random
from violas_client import Client, Wallet

client = Client("violas_testnet")
wallet = Wallet.new()
addr = "b14bc3286e4b9b41c86022f2e614d721"
state = client.get_account_state(addr)
# print(state.get_tokens_resource())
# print(client.bank_get_lock_amounts(addr))
# print(client.bank_get_borrow_amounts(addr))
# random.randint(100_000_000, 1_000_000_000_000)
# client.mint_coin("b14bc3286e4b9b41c86022f2e614d721", 1_000_000_000, currency_code="vBTC")
# client.mint_coin("b14bc3286e4b9b41c86022f2e614d721", 1_000_000_000, currency_code="vUSDT")




