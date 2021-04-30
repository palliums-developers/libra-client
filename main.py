import random
import time
from libra_client import Client, Wallet

cli = Client()
w = Wallet.new()
a1 = w.new_account()
# cli.mint_coin(a1.address_hex, 22, auth_key_prefix=a1.auth_key_prefix, currency_code="VLS")
# balances = cli.get_balances(a1.address_hex)
# assert balances["VLS"] == 22