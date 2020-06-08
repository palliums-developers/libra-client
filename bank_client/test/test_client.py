from bank_client import Client, Wallet
import time
module_address = "3e7f951e8f86a8b8c2aff288aa99753c"

def approximately_equal_to(a, b):
    a = int(a)
    b = int(b)
    return a in (b+1, b, b-1)

def publish_bank_module():
    wallet = Wallet.new()
    module_account = wallet.new_account()
    client = Client("bj_testnet")
    client.mint_coin(module_account.address, 2_000_000_000, auth_key_prefix=module_account.auth_key_prefix)
    client.publish_bank(module_account)
    client.set_bank_module_address(module_account.address)
    client.publish(module_account)
    client.register_token(module_account, module_account.address, 0.5, currency_code="LBR")
    client.register_token(module_account, module_account.address, 0.5, currency_code="Coin1")
    client.register_token(module_account, module_account.address, 0.5, currency_code="Coin2")

    client.update_price(module_account, 0.1, currency_code="LBR")
    client.update_price(module_account, 0.1, currency_code="LBR")
    client.update_price(module_account, 0.1, currency_code="LBR")
    return module_account.address_hex

def test_init():
    address = publish_bank_module()
    print(address)

def test_lock():
    client = Client("bj_testnet")
    wallet = Wallet.new()
    a1 = wallet.new_account()
    module_address = publish_bank_module()
    client.set_bank_module_address(module_address)
    client.mint_coin(a1.address, 2_000_000_000, auth_key_prefix=a1.auth_key_prefix)
    client.publish(a1)
    client.enter_bank(a1, 2_000_000_000)
    client.lock(a1, 1_000_000_000)
    assert 1_000_000_000 == client.get_bank_amount(a1.address)
    assert approximately_equal_to(client.get_lock_amount(a1.address), 1_000_000_000)
    assert 0 == client.get_cur_lock_rate()

def test_redeem():
    client = Client("bj_testnet")
    wallet = Wallet.new()
    a1 = wallet.new_account()
    module_address = publish_bank_module()
    client.set_bank_module_address(module_address)
    client.mint_coin(a1.address, 2_000_000_000, auth_key_prefix=a1.auth_key_prefix)
    client.publish(a1)
    client.enter_bank(a1, 2_000_000_000)
    client.lock(a1, 1_000_000_000)
    time.sleep(60)
    client.redeem(a1)
    assert approximately_equal_to(client.get_bank_amount(a1.address), 2_000_000_000)

def test_borrow():
    client = Client("bj_testnet")
    wallet = Wallet.new()
    a1 = wallet.new_account()
    module_address = publish_bank_module()
    client.set_bank_module_address(module_address)
    client.mint_coin(a1.address, 2_000_000_000, auth_key_prefix=a1.auth_key_prefix)
    client.publish(a1)
    client.enter_bank(a1, 2_000_000_000)
    client.lock(a1, 1_000_000_000)
    client.borrow(a1, 100_000_000)
    assert approximately_equal_to(client.get_borrow_amount(a1.address), 100_000_000)
    assert approximately_equal_to(client.get_bank_amount(a1.address), 1_000_000_000+100_000_000)

def test_repay_borrow():
    client = Client("bj_testnet")
    wallet = Wallet.new()
    a1 = wallet.new_account()
    module_address = publish_bank_module()
    client.set_bank_module_address(module_address)
    client.mint_coin(a1.address, 2_000_000_000, auth_key_prefix=a1.auth_key_prefix)
    client.publish(a1)
    client.enter_bank(a1, 2_000_000_000)
    client.lock(a1, 1_000_000_000)
    client.borrow(a1, 100_000_000)
    client.repay_borrow(a1)
    assert approximately_equal_to(client.get_borrow_amount(a1.address), 0)
    assert approximately_equal_to(client.get_bank_amount(a1.address), 1_000_000_000)

def test_get_cur_lock_rate():
    client = Client("bj_testnet")
    wallet = Wallet.new()
    a1 = wallet.new_account()
    a2 = wallet.new_account()
    module_address = publish_bank_module()
    client.set_bank_module_address(module_address)
    client.mint_coin(a1.address, 2_000_000_000, auth_key_prefix=a1.auth_key_prefix)
    client.mint_coin(a2.address, 2_000_000_000, auth_key_prefix=a2.auth_key_prefix)

    client.publish(a1)
    client.publish(a2)

    client.enter_bank(a1, 2_000_000_000)
    client.enter_bank(a2, 2_000_000_000)

    client.lock(a1, 1_000_000_000)
    client.borrow(a1, 100_000_000)

    client.lock(a2, 1_000_000_000)

    lock_rate = client.get_cur_lock_rate()
    time.sleep(60)
    lock_amount = client.get_lock_amount(a2.address)
    assert approximately_equal_to(lock_amount, 1_000_000_000+1_000_000_000*lock_rate)
    client.redeem(a2)
    assert approximately_equal_to(2_000_000_000+lock_amount-1_000_000_000, client.get_bank_amount(a2.address))

def test_get_cur_borrow_rate():
    client = Client("bj_testnet")
    wallet = Wallet.new()
    a1 = wallet.new_account()
    module_address = publish_bank_module()
    client.set_bank_module_address(module_address)
    client.mint_coin(a1.address, 2_000_000_000, auth_key_prefix=a1.auth_key_prefix)
    client.publish(a1)
    client.enter_bank(a1, 2_000_000_000)
    client.lock(a1, 1_000_000_000)
    client.borrow(a1, 100_000_000)
    borrow_rate = client.get_cur_borrow_rate()
    time.sleep(120)
    borrow_amount = client.get_borrow_amount(a1.address)
    assert approximately_equal_to(borrow_amount, 100_000_000+100_000_000*borrow_rate*2)
    client.repay_borrow(a1)
    assert approximately_equal_to(client.get_bank_amount(a1.address), 1_000_000_000-100_000_000*borrow_rate*2)

