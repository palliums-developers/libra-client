import random
import time
from violas_client import Client, Wallet


client = Client("violas_testnet")
state = client.get_account_state(client.get_exchange_owner_address())
print(state.get_tokens_resource())
# print(state.swap_get_reward_pools())