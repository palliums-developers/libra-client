from violas_client import Client, Wallet

client = Client("bj_testnet")
print(client.get_account_state(client.get_bank_owner_address()).get_token_info_store_resource())