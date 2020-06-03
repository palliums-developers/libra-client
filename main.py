from compound_client import Client, Wallet
module_address = "414dbe6aab9cef746500d5e19dbc0a64"

# client = Client("bj_testnet")
# wallet = Wallet.new()
# while True:
#     import time
#     a1 = wallet.new_account()
#     client.set_bank_module_address(module_address)
#     client.mint_coin(a1.address_hex, 10 ** 12, auth_key_prefix=a1.auth_key_prefix, currency_code="LBR")
#     client.compound_publish(a1, bank_module_address=module_address)
#     client.compound_enter_bank(a1, 10 ** 12, currency_code="LBR")
#     print(client.get_bank_amount(a1.address_hex))
#     client.compound_lock(a1, 10**10, currency_code="LBR")
#     client.compound_borrow(a1, 10**9)
#     client.compound_repay_borrow(a1, 0)
#     print(client.get_bank_amount(a1.address_hex))
#     print(client.get_borrowed_amount(a1.address_hex))


client = Client("bj_testnet")
wallet = Wallet.new()
a1 = wallet.new_account()
client.set_bank_module_address(module_address)
client.mint_coin(a1.address_hex, 10 ** 15, auth_key_prefix=a1.auth_key_prefix, currency_code="LBR")
client.compound_publish(a1, bank_module_address=module_address)
client.compound_enter_bank(a1, 10 ** 15, currency_code="LBR")


client.compound_lock(a1, 10**15, currency_code="LBR")
client.compound_borrow(a1, 10**9)

turn = 0
while True:
    import time
    print("borrow_amount = ", client.get_borrowed_amount(a1.address_hex))
    print("locked_amount = ", client.get_locked_amount(a1.address_hex))
    print(turn)
    turn = turn+1
    time.sleep(60)














