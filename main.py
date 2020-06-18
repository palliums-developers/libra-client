from libra_client import Client, Wallet
from lbrtypes.account_config import treasury_compliance_account_address, association_address
from typing import List
from libra_client.account import Account

client = Client()
print(client.get_currency_info("Coin1"))