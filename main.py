import random
import time
from violas_client import Client, Wallet


import argparse
from violas_client import Client


#client = Client("bj_testnet")
client = Client("violas_testnet")
#print(client.get_account_state(args.address))
state = client.get_account_state("b9389af0b00349e319d5110ecc9bc307")
print(state)
print("---------------------------------------------")
print("---------------------------------------------")
print("---------------------------------------------")

#print(state.get_token_info_store_resource(accrue_interest=False))

print(state.swap_get_reserves_resource())
print(state.swap_get_tokens_resource())
print(state.swap_get_reward_pools())
print(state.swap_get_pool_user_infos())