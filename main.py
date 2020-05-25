from compound_client import Client, Wallet

client = Client()
wallet = Wallet.new()
module_account = wallet.new_account()

module_account = wallet.new_account()
client.mint_coin(module_account.address, 1_000_000, auth_key_prefix=module_account.auth_key_prefix)
client.publish_bank(module_account)
client.publish(module_account, bank_module_address=module_account.address)
state = client.get_account_state(module_account.address)
print(state.get_tokens_resource)















