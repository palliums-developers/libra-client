from violas_client import Client, Wallet
from violas_client.banktypes.bytecode import CodeType


client = Client("bj_testnet")

def test_get_code_type():
    wallet = Wallet.new()

    a1 = wallet.new_account()
    client.mint_coin(a1.address, 300_000_000, auth_key_prefix=a1.auth_key_prefix, currency_code="VUSDT")
    seq = client.bank_publish(a1)
    assert client.get_account_transaction(a1.address, seq).get_code_type() == CodeType.PUBLISH

    seq = client.bank_lock2(a1, 100_000_000, currency_code="VUSDT")
    assert client.get_account_transaction(a1.address, seq).get_code_type() == CodeType.LOCK2

    seq = client.bank_borrow2(a1, 1_000, currency_code="VUSDT")
    assert client.get_account_transaction(a1.address, seq).get_code_type() == CodeType.BORROW2
    _, amount = client.bank_get_borrow_amount(a1.address, currency_code="VUSDT")
    seq = client.bank_repay_borrow2(a1, currency_code="VUSDT", amount=amount)
    assert client.get_account_transaction(a1.address, seq).get_code_type() == CodeType.REPAY_BORROW2
    amount = client.bank_get_lock_amount(a1.address, currency_code="VUSDT")
    seq = client.bank_redeem2(a1, currency_code="VUSDT", amount=amount)
    assert client.get_account_transaction(a1.address, seq).get_code_type() == CodeType.REDEEM2

def test_get_amount():
    wallet = Wallet.new()
    
    a1 = wallet.new_account()
    client.mint_coin(a1.address, 300_000_000, auth_key_prefix=a1.auth_key_prefix, currency_code="VUSDT")
    seq = client.bank_publish(a1)
    assert client.get_account_transaction(a1.address, seq).get_amount() == None

    seq = client.bank_lock2(a1, 100_000_000, currency_code="VUSDT")
    assert client.get_account_transaction(a1.address, seq).get_amount() == 100_000_000

    seq = client.bank_borrow2(a1, 1_000, currency_code="VUSDT")
    assert client.get_account_transaction(a1.address, seq).get_amount() == 1_000

    seq = client.bank_repay_borrow2(a1, amount=100, currency_code="VUSDT")
    assert client.get_account_transaction(a1.address, seq).get_amount() == 100

    seq = client.bank_redeem2(a1, currency_code="VUSDT", amount=100)
    assert client.get_account_transaction(a1.address, seq).get_amount() == 100

def test_get_currency_code():
    wallet = Wallet.new()

    a1 = wallet.new_account()
    client.mint_coin(a1.address, 300_000_000, auth_key_prefix=a1.auth_key_prefix, currency_code="VUSDT")
    seq = client.bank_publish(a1)
    assert client.get_account_transaction(a1.address, seq).get_currency_code() == None

    seq = client.bank_lock2(a1, 100_000_000, currency_code="VUSDT")
    assert client.get_account_transaction(a1.address, seq).get_currency_code() == "VUSDT"

    seq = client.bank_borrow2(a1, 1_000, currency_code="VUSDT")
    assert client.get_account_transaction(a1.address, seq).get_currency_code() == "VUSDT"

    seq = client.bank_repay_borrow2(a1, amount=100, currency_code="VUSDT")
    assert client.get_account_transaction(a1.address, seq).get_currency_code() == "VUSDT"

    seq = client.bank_redeem2(a1, amount=100, currency_code="VUSDT")
    assert client.get_account_transaction(a1.address, seq).get_currency_code() == "VUSDT"

def test_get_data():
    data = "data"
    data_hex = b"data".hex()
    wallet = Wallet.new()

    a1 = wallet.new_account()
    client.mint_coin(a1.address, 300_000_000, auth_key_prefix=a1.auth_key_prefix, currency_code="VUSDT")
    seq = client.bank_publish(a1, data=data)
    assert client.get_account_transaction(a1.address, seq).get_data() == data_hex

    seq = client.bank_lock2(a1, 100_000_000, currency_code="VUSDT", data=data)
    assert client.get_account_transaction(a1.address, seq).get_data() == data_hex

    seq = client.bank_borrow2(a1, 1_000, currency_code="VUSDT", data=data)
    assert client.get_account_transaction(a1.address, seq).get_data() == data_hex

    seq = client.bank_repay_borrow2(a1, amount=100, currency_code="VUSDT", data=data)
    assert client.get_account_transaction(a1.address, seq).get_data() == data_hex

    seq = client.bank_redeem2(a1, amount=100, currency_code="VUSDT", data=data)
    assert client.get_account_transaction(a1.address, seq).get_data() == data_hex


def test_get_incentive():
    wallet = Wallet.new()

    a1 = wallet.new_account()
    client.mint_coin(a1.address, 300_000_000, auth_key_prefix=a1.auth_key_prefix, currency_code="VUSDT")
    seq = client.bank_publish(a1)
    assert client.get_account_transaction(a1.address, seq).get_currency_code() == None

    client.bank_lock2(a1, 100_000_000, currency_code="VUSDT")

    seq = client.bank_borrow2(a1, 1_000_000, currency_code="VUSDT")
    tx = client.get_account_transaction(a1.address, seq)
    assert tx.get_incentive() != None

    seq = client.bank_repay_borrow2(a1, amount=100, currency_code="VUSDT")
    tx = client.get_account_transaction(a1.address, seq)
    assert tx.get_incentive() != None

    seq = client.bank_redeem2(a1, amount=100, currency_code="VUSDT")
    tx = client.get_account_transaction(a1.address, seq)
    assert tx.get_incentive() != None