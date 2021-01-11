import random
from violas_client import Client, Wallet

client = Client("violas_testnet")
wallet = Wallet.new()
# random.randint(100_000_000, 1_000_000_000_000)
# client.mint_coin("b14bc3286e4b9b41c86022f2e614d721", 1_000_000_000, currency_code="vBTC")
# client.mint_coin("b14bc3286e4b9b41c86022f2e614d721", 1_000_000_000, currency_code="vUSDT")

i = 0
while True:
    a1 = wallet.new_account()
    v1 = random.randint(100_000_000, 1_000_000_000_000)
    client.mint_coin(a1.address, v1, currency_code="vBTC", auth_key_prefix=a1.auth_key_prefix, add_all_currencies=True)
    v2 = random.randint(100_000_000, 1_000_000_000_000)
    client.add_currency_to_account(a1, "vUSDT")
    client.mint_coin(a1.address, v2, currency_code="vUSDT", auth_key_prefix=a1.auth_key_prefix, add_all_currencies=True)
    client.bank_publish(a1)
    client.bank_lock(a1, v1, currency_code="vBTC")
    client.bank_lock(a1, v2, currency_code="vUSDT")

    client.bank_borrow(a1, int(v1/2 - 1_000_000), currency_code="vBTC")
    client.bank_borrow(a1, int(v2/2 - 1_000_000), currency_code="vUSDT")
    print(i)
    i += 1



