from violas_client import Client, Wallet
import time
from enum import IntEnum

wallet = Wallet.new()
client = Client()
txs = client.get_transactions(20273500, 500)
for tx in txs:
    code = tx.get_currency_code()
    if code is not None:
        print(tx.get_version(), tx.get_code_type(), tx.get_currency_code())

