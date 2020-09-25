from json_rpc.views import TransactionView, EventView
from lbrtypes.account_state import AccountState
from error.error import LibraError
from lbrtypes.account_config import testnet_dd_account_address
from libra_client import Client, Wallet
from typing import List
from libra_client.account import Account

def create_accounts(account_number)-> List[Account]:
    wallet = Wallet.new()
    return [wallet.new_account() for _ in range(account_number)]

def create_accounts_with_coins(account_number)-> List[Account]:
    wallet = Wallet.new()
    client = create_client()
    accounts = []
    for _ in range(account_number):
        account = wallet.new_account()
        client.mint_coin(account.address, 100, auth_key_prefix=account.auth_key_prefix, is_blocking=True)
        accounts.append(account)
    return accounts

def create_client() -> Client:
    return Client()

def test_get_balance():
    [a1] = create_accounts(1)
    client = create_client()
    balance = client.get_balance(a1.address)
    assert balance == 0

    client.mint_coin(a1.address, 100, auth_key_prefix=a1.auth_key_prefix, is_blocking=True)
    balance = client.get_balance(a1.address)
    assert balance == 100

def test_get_balances():
    [a1] = create_accounts(1)
    client = create_client()
    client.mint_coin(a1.address_hex, 11, auth_key_prefix=a1.auth_key_prefix, currency_code="LBR")
    client.add_currency_to_account(a1, "Coin1")
    client.mint_coin(a1.address_hex, 22, auth_key_prefix=a1.auth_key_prefix, currency_code="Coin1")
    balances = client.get_balances(a1.address_hex)
    assert balances["LBR"] == 11
    assert balances["Coin1"] == 22

test_get_balances()