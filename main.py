import random
import time
from violas_client import Client, Wallet


client = Client("violas_testnet")
chain_token_infos = client.get_account_state(client.get_bank_owner_address(), 705117).get_token_info_store_resource(accrue_interest=False).tokens
print(chain_token_infos)