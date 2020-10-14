from violas_client import Client, Wallet
from libra_client.lbrtypes.transaction.script import Script


client = Client("bj_testnet")
print(client.get_transaction(22142919).get_currency_code())
# info = client.get_account_state(client.BANK_OWNER_ADDRESS).get_token_info_store_resource(accrue_interest=False)
# print(info)
# wallet = Wallet.new()
# a1 = wallet.new_account()
# client.mint_coin(a1.address_hex, 1000, auth_key_prefix=a1.auth_key_prefix, currency_code="LBR")
# client.bank_publish(a1)
# client.bank_update_price_from_oracle(a1, "USD", gas_currency_code="LBR")
# token_infos = client.oracle_get_exchange_rate("VLSUSD")
# print(client.get_transaction(17150941).get_code_type())