from violas_client import Client, Wallet
import time

client =Client()

wallet = Wallet.new()
module_account = wallet.new_account()
client.mint_coin(module_account.address, 200_000_000, auth_key_prefix=module_account.auth_key_prefix,
                 currency_code="USD")
seq = client.bank_publish(module_account)
assert client.get_account_transaction(module_account.address, seq).get_amount() == None

a1 = wallet.new_account()
client.mint_coin(a1.address, 300_000_000, auth_key_prefix=a1.auth_key_prefix, currency_code="USD")
client.add_currency_to_account(a1, "VLS")
seq = client.bank_publish(a1)
seq = client.bank_lock(a1, 100_000_000, currency_code="USD")
time.sleep(60)
print(client.bank_get_sum_incentive_amount(a1.address_hex))
seq = client.bank_redeem(a1, 100_000_000 ,currency_code="USD")
tx = client.get_account_transaction(a1.address_hex, seq)
print(tx.get_incentive())
