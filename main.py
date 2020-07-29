from libra_client import Client
from libra_client.wallet_library import Wallet

client = Client()
wallet = Wallet.new()
module_account = wallet.new_account()
client.mint_coin(module_account.address, 2_000, auth_key_prefix=module_account.auth_key_prefix)
# client.bank_publish_contract(module_account)
# client.set_bank_module_address(module_account.address)
# client.bank_publish(module_account)
# client.bank_register_token(module_account, module_account.address, 0.5, currency_code="LBR")
# client.bank_register_token(module_account, module_account.address, 0.5, currency_code="Coin1")
# client.bank_register_token(module_account, module_account.address, 0.5, currency_code="Coin2")
#
# client.bank_update_price(module_account, 0.1, currency_code="LBR")
# client.bank_update_price(module_account, 0.1, currency_code="LBR")
# client.bank_update_price(module_account, 0.1, currency_code="LBR")
