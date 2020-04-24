from test import create_accounts, create_client, create_accounts_with_coins
from error import ViolasError
from libra.transaction import Script, TransactionPayload, SignedTransaction
from json_rpc.views import AccountView, TransactionView, EventView
from libra.account_config import AccountConfig

def test_get_sender():
    client = create_client()
    [a1, a2] = create_accounts(2)
    seq = client.mint_coin(a1.address, 100, receiver_auth_key_prefix_opt=a1.auth_key_prefix, is_blocking=True)
    tx = client.get_account_transaction(AccountConfig.association_address(), seq)
    assert tx.get_sender() == AccountConfig.association_address()

    seq = client.transfer_coin(a1, 10, a2.address, receiver_auth_key_prefix_opt=a2.auth_key_prefix, is_blocking=True)
    tx = client.get_account_transaction(a1.address, seq)
    assert tx.get_sender() == a1.address_hex

    tx = client.get_transaction(0)
    assert None == tx.get_sender()

    tx = client.get_transaction(1)
    assert None == tx.get_sender()

def test_get_receiver():
    client = create_client()
    [a1, a2] = create_accounts(2)
    seq = client.mint_coin(a1.address, 100, receiver_auth_key_prefix_opt=a1.auth_key_prefix, is_blocking=True)
    tx = client.get_account_transaction(AccountConfig.association_address(), seq)
    assert tx.get_receiver() == a1.address_hex

    seq = client.transfer_coin(a1, 10, a2.address, receiver_auth_key_prefix_opt=a2.auth_key_prefix, is_blocking=True)
    tx = client.get_account_transaction(a1.address, seq)
    assert tx.get_receiver() == a2.address_hex

    tx = client.get_transaction(0)
    assert None == tx.get_receiver()

    tx = client.get_transaction(1)
    assert None == tx.get_receiver()

def test_get_amount():
    client = create_client()
    [a1, a2] = create_accounts(2)
    seq = client.mint_coin(a1.address, 99, receiver_auth_key_prefix_opt=a1.auth_key_prefix, is_blocking=True)
    tx = client.get_account_transaction(AccountConfig.association_address(), seq)
    assert tx.get_amount() == 99

    seq = client.transfer_coin(a1, 88, a2.address, receiver_auth_key_prefix_opt=a2.auth_key_prefix, is_blocking=True)
    tx = client.get_account_transaction(a1.address, seq)
    assert tx.get_amount() == 88

    tx = client.get_transaction(0)
    assert None == tx.get_amount()

    tx = client.get_transaction(1)
    assert None == tx.get_amount()

def test_get_data():
    client = create_client()
    [a1, a2] = create_accounts(2)
    seq = client.mint_coin(a1.address, 100, receiver_auth_key_prefix_opt=a1.auth_key_prefix, is_blocking=True)
    tx = client.get_account_transaction(AccountConfig.association_address(), seq)
    assert tx.get_data() == None

    data = b"data"
    seq = client.transfer_coin(a1, 10, a2.address, receiver_auth_key_prefix_opt=a2.auth_key_prefix, is_blocking=True, data=data)
    tx = client.get_account_transaction(a1.address, seq)
    assert tx.get_data() == data.hex()

    seq = client.transfer_coin(a1, 10, a2.address, receiver_auth_key_prefix_opt=a2.auth_key_prefix, is_blocking=True)
    tx = client.get_account_transaction(a1.address, seq)
    assert tx.get_data() == ""

    tx = client.get_transaction(0)
    assert None == tx.get_data()

    tx = client.get_transaction(1)
    assert None == tx.get_data()