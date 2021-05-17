import pytest
from violas_client.exchange_client import Wallet, Client


@pytest.fixture
def client():
    return Client("bj_testnet")

@pytest.fixture
def liquidity_account(client):
    wallet = Wallet.new()
    liquidity_account = wallet.new_account()
    client.mint_coin(liquidity_account.address, 100_000_000, auth_key_prefix=liquidity_account.auth_key_prefix, is_blocking=True, currency_code="VUSDT")
    client.add_currency_to_account(liquidity_account, "VBTC")
    client.mint_coin(liquidity_account.address, 100_000_000, currency_code="VBTC", auth_key_prefix=liquidity_account.auth_key_prefix, is_blocking=True)
    client.add_currency_to_account(liquidity_account, "VLS")
    return liquidity_account

@pytest.fixture
def swap_account(client):
    wallet = Wallet.new()
    swap_account = wallet.new_account()
    client.mint_coin(swap_account.address, 10_000_000, auth_key_prefix=swap_account.auth_key_prefix, is_blocking=True, currency_code="VUSDT")
    client.add_currency_to_account(swap_account, "VBTC")
    client.mint_coin(swap_account.address, 10_000_000, currency_code="VBTC", auth_key_prefix=swap_account.auth_key_prefix, is_blocking=True)
    return swap_account

def test_add_liquidity(client, liquidity_account, swap_account):
    VUSDT_before_balance = client.get_balance(liquidity_account.address, "VUSDT")
    VBTC_before_balance = client.get_balance(liquidity_account.address, "VBTC")
    client.swap_add_liquidity(liquidity_account, "VUSDT", "VBTC", 1_000_000, 321_432)
    VUSDT_after_balance = client.get_balance(liquidity_account.address, "VUSDT")
    VBTC_after_balance = client.get_balance(liquidity_account.address, "VBTC")
    assert VUSDT_before_balance - VUSDT_after_balance == 1_000_000 or VBTC_before_balance - VBTC_after_balance == 321_432

def test_remove_liquidity(client, liquidity_account, swap_account):
    client.swap_add_liquidity(liquidity_account, "VUSDT", "VBTC", 1_000_000, 321_432)
    values = client.swap_get_liquidity_balances(liquidity_account.address)[0]
    client.swap_remove_liquidity(liquidity_account, "VBTC", "VUSDT", values["liquidity"])

def test_swap(client, liquidity_account, swap_account):

    client.swap_add_liquidity(liquidity_account, "VUSDT", "VBTC", 123_321, 321_432)
    (expected_amount, out) = client.swap_get_swap_output_amount("VBTC", "VUSDT", 1000)
    before_amount = client.get_balance(swap_account.address, "VUSDT")
    client.swap(swap_account, "VBTC", "VUSDT", 1000, expected_amount)
    after_amount = client.get_balance(swap_account.address, "VUSDT")
    assert after_amount - before_amount == expected_amount


def test_swap_get_liquidity_balances(client, liquidity_account, swap_account):
    client.swap_add_liquidity(liquidity_account, "VUSDT", "VBTC", 2344532, 342566)
    client.swap(swap_account, "VBTC", "VUSDT", 1000)
    blb = client.get_balance(liquidity_account.address, "VUSDT")
    bc1b = client.get_balance(liquidity_account.address, "VBTC")
    all = client.swap_get_liquidity_balances(liquidity_account.address)[0]
    client.swap_remove_liquidity(liquidity_account, "VBTC", "VUSDT", all["liquidity"])
    alb = client.get_balance(liquidity_account.address, "VUSDT")
    ac1b = client.get_balance(liquidity_account.address, "VBTC")
    assert alb - blb == all["VUSDT"]
    assert ac1b - bc1b == all["VBTC"]

def test_swap_get_swap_output_amount(client, liquidity_account, swap_account):

    client.swap_add_liquidity(liquidity_account, "VUSDT", "VBTC", 342423, 435435)
    out, _ = client.swap_get_swap_output_amount("VBTC", "VUSDT", 100_000)
    bb = client.get_balance(swap_account.address, "VUSDT")
    client.swap(swap_account, "VBTC", "VUSDT", 100_000)
    ab = client.get_balance(swap_account.address, "VUSDT")
    assert ab - bb == out

def test_swap_get_swap_input_amount(client, liquidity_account, swap_account):
    client.swap_add_liquidity(liquidity_account, "VUSDT", "VBTC", 3243244, 4354435)
    out, _ = client.swap_get_swap_input_amount("VBTC", "VUSDT", 243444)
    bb = client.get_balance(swap_account.address, "VUSDT")
    client.swap(swap_account, "VBTC", "VUSDT", out)
    ab = client.get_balance(swap_account.address, "VUSDT")
    assert 243444-1 <= ab - bb <= 243444+1

def test_swap_get_liquidity_output_amount(client, liquidity_account, swap_account):
    client.swap_add_liquidity(liquidity_account, "VUSDT", "VBTC", 3243243, 432432)
    out = client.swap_get_liquidity_output_amount("VBTC", "VUSDT", 243244)
    bc1b = client.get_balance(liquidity_account.address, "VBTC")
    client.swap_add_liquidity(liquidity_account, "VUSDT", "VBTC", out, 1000000000)
    ac1b = client.get_balance(liquidity_account.address, "VBTC")
    assert bc1b - ac1b == 243244

def test_withdraw_mine_reward(client, liquidity_account):

    amount = client.swap_get_reward_balance(liquidity_account.address_hex)
    seq = client.swap_withdraw_mine_reward(liquidity_account)
    tx = client.get_account_transaction(liquidity_account.address_hex, seq)
    assert amount == tx.get_swap_reward_amount()


