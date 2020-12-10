from violas_client import Client, Wallet
import time

client = Client()
# v = client.get_account_state(client.BANK_OWNER_ADDRESS).get_token_info_store_resource(accrue_interest=False)
# print(v)
wallet = Wallet.new()
a1 = wallet.new_account()
client.mint_coin(a1.address, 300_000_000, auth_key_prefix=a1.auth_key_prefix, currency_code="EUR")
client.add_currency_to_account(a1, "VLS")
client.bank_publish(a1)
client.bank_lock(a1, 100_000_000, currency_code="EUR")
client.bank_borrow(a1, 10_000_000, currency_code="EUR")
seq = client.claim_incentive(a1)
tx = client.get_account_transaction(a1.address, seq)
print(tx.get_incentive())
# borrow_rate = client.bank_get_borrow_rate(currency_code="EUR")
# _, borrow_amount = client.bank_get_borrow_amount(a1.address, currency_code="EUR")
# client.bank_repay_borrow(a1, amount=borrow_amount, currency_code="EUR")
# assert client.bank_get_borrow_amount(a1.address, "EUR")[0] == 0
#
# # from libra_client import Wallet
# # mn = "chalk cereal gate tape near stamp candy liberty insect pyramid toward uphold punch almost lift blur pledge lobster genuine file chief awkward drama govern"
# # mn = "buffalo become better swarm motion margin reward twice develop judge cancel garage document actor ceiling tornado mom busy cloth position equal parrot surface network"
# # wallet = Wallet.new_from_mnemonic(mn)
# # print(wallet.new_account().address_hex)