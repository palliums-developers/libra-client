from compound_client import Client, Wallet

module_address = "3e7f951e8f86a8b8c2aff288aa99753c"

def test_init():
    wallet = Wallet.new()
    module_account = wallet.new_account()
    client = Client("bj_testnet")
    client.mint_coin(module_account.address, 2_000_000_000, auth_key_prefix=module_account.auth_key_prefix)
    client.compound_publish_bank(module_account)
    client.set_bank_module_address(module_account.address)
    client.compound_publish(module_account)
    client.compound_register_token(module_account, module_account.address, 0.5, currency_code="LBR")
    client.compound_register_token(module_account, module_account.address, 0.5, currency_code="Coin1")
    client.compound_register_token(module_account, module_account.address, 0.5, currency_code="Coin2")

    client.compound_update_price(module_account, 1, currency_code="LBR")
    client.compound_update_price(module_account, 1, currency_code="LBR")
    client.compound_update_price(module_account, 1, currency_code="LBR")
    print(module_account.address_hex)



def test_compound_lock():
    client = Client("bj_testnet")
    wallet = Wallet.new()
    a1 = wallet.new_account()
    client.set_bank_module_address(module_address)
    client.mint_coin(a1.address_hex, 10**6, auth_key_prefix=a1.auth_key_prefix, currency_code="LBR")
    client.compound_publish(a1, bank_module_address=module_address)
    client.compound_enter_bank(a1, 10**5, currency_code="LBR")
    client.compound_lock(a1, 10**5, currency_code="LBR")
    assert client.get_balance(a1.address_hex) == 10**6 - 10**5
    assert client.get_deposit_amount(a1.address_hex, currency_code="LBR") == 10**5
