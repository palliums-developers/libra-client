# from violas_client import Client, Wallet
# from violas_client.lbrtypes.account_config import treasury_compliance_account_address, association_address
from exchange_client import Client, Wallet
from lbrtypes.account_config import treasury_compliance_account_address, association_address
import time
from move_core_types.language_storage import core_code_address

# coins = ['Coin1', 'Coin2',  'VLSUSD', 'VLSEUR', 'VLSGBP', 'VLSSGD', 'VLS', 'USD', 'EUR', 'GBP', 'SGD', 'BTC']
coins = ['Coin1', 'Coin2',  'VLSUSD', 'VLSEUR', 'VLSGBP', 'VLSSGD', 'VLS', 'USD', 'EUR', 'GBP', 'SGD', 'BTC']


coin_pairs = []
pre_coin = None
coin_len = len(coins)
for i in range(len(coins)):
    for start in range(i+1, len(coins)):
        coin_pairs.append((coins[i], coins[start]))
wallet = Wallet.new()
client = Client("violas_testnet")
module_account = wallet.new_account()
liquity_account = wallet.new_account()
client.mint_coin(module_account.address, 10_000_000, auth_key_prefix=module_account.auth_key_prefix, is_blocking=True)
client.mint_coin(liquity_account.address, 10_000_000_000, auth_key_prefix=liquity_account.auth_key_prefix)

client.swap_publish_contract(module_account)
client.set_exchange_module_address(module_account.address)
seq = client.swap_initialize(module_account)

for coin in coins:
    client.swap_add_currency(module_account, coin)
    if coin != "LBR":
        client.add_currency_to_account(liquity_account, coin, gas_currency_code="LBR")
        client.mint_coin(liquity_account.address, 10_000_000_000, auth_key_prefix=liquity_account.auth_key_prefix, currency_code=coin)

for coin_pair in coin_pairs:
    client.swap_add_liquidity(liquity_account, coin_pair[0], coin_pair[1], 1_000_000, 1_000_000)


print(client.get_index_max_output_path(0,1,100))
