from bank_client import Client, Wallet
module_address = "9653aa71723b1d340378b01981e607d4"

client = Client("bj_testnet")
wallet = Wallet.new()

module_account = wallet.new_account()
module_address = module_account.address_hex
client.mint_coin(module_account.address, 2_000_000_000, auth_key_prefix=module_account.auth_key_prefix)
client.publish_bank(module_account)
client.set_bank_module_address(module_account.address)
client.publish(module_account)
client.register_token(module_account, module_account.address, 0.5, currency_code="LBR")
client.update_price(module_account, 0.1, currency_code="LBR")

a1 = wallet.new_account()
a2 = wallet.new_account()

client.set_bank_module_address(module_address)
client.mint_coin(a1.address_hex, 10 ** 15, auth_key_prefix=a1.auth_key_prefix, currency_code="LBR")
client.mint_coin(a2.address_hex, 10 ** 15, auth_key_prefix=a2.auth_key_prefix, currency_code="LBR")

client.publish(a1, bank_module_address=module_address)
client.publish(a2, bank_module_address=module_address)

client.enter_bank(a1, 10 ** 15, currency_code="LBR")
client.enter_bank(a2, 10 ** 15, currency_code="LBR")


client.lock(a1, 10**14, currency_code="LBR")
client.lock(a2, 10**14, currency_code="LBR")

client.borrow(a1, 10**13)

turn = 0
while True:
    import time
    print(client.get_account_state(module_address).get_utilization("LBR"))
    time.sleep(60)
    # borrow_amount = client.get_borrow_amount(a1.address_hex, include_interest=False)
    # locked_amount = client.get_lock_amount(a1.address_hex)
    # total_supply = client.get_account_state(module_address).get_total_supplied_balance("LBR")
    # total_borrow = client.get_account_state(module_address).get_total_borrows_balance("LBR")
    # total_reserve = client.get_account_state(module_address).get_reserves("LBR")
    # lock_apr = client.get_account_state(module_address).get_cur_lock_rate("LBR")
    #
    # time.sleep(60)
    #
    # borrow_amount2 = client.get_borrow_amount(a1.address_hex)
    # locked_amount2 = client.get_lock_amount(a1.address_hex)
    # total_supply2 = client.get_account_state(module_address).get_total_supplied_balance("LBR")
    # total_borrow2 = client.get_account_state(module_address).get_total_borrows_balance("LBR")
    # total_reserve2 = client.get_account_state(module_address).get_reserves("LBR")
    # lock_apr2 = client.get_account_state(module_address).get_cur_lock_rate("LBR")
    #
    # print(f"lock1 = {locked_amount}, lock2={locked_amount2}, lock_amount_diff = {locked_amount2-locked_amount}")
    # print(f"locked_amount_diff = {locked_amount2-locked_amount}")
    # print(f"lock_amount2={locked_amount2} , lock_apr = {lock_apr}, lock_sum = {locked_amount+locked_amount*lock_apr}")
    #
    # print("..............................")














