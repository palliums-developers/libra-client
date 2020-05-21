from test import create_accounts, create_client, create_accounts_with_coins
from json_rpc.views import TransactionView, EventView
from lbrtypes.account_state import AccountState
from error import LibraError
from lbrtypes.account_config import association_address

def test_get_balance():
    [a1] = create_accounts(1)
    client = create_client()
    balance = client.get_balance(a1.address)
    assert balance == 0

    client.mint_coin(a1.address, 100, auth_key_prefix=a1.auth_key_prefix, is_blocking=True)
    balance = client.get_balance(a1.address)
    assert balance == 100

def test_get_sequence_number():
    a1, a2 = create_accounts(2)
    client = create_client()
    seq = client.get_sequence_number(a1.address)
    assert 0 == seq
    client.mint_coin(a1.address, 100, auth_key_prefix=a1.auth_key_prefix, is_blocking=True)
    seq = client.get_sequence_number(a1.address)
    assert 0 == seq
    client.transfer_coin(a1, a2.address, 10,  auth_key_prefix=a2.auth_key_prefix, is_blocking=True)
    seq = client.get_sequence_number(a1.address)
    assert 1 == seq

def test_mint_coin():
    [a1] = create_accounts(1)
    client = create_client()
    try:
        client.mint_coin(a1.address, 100, is_blocking=True)
        assert 0
    except LibraError as e:
        print("Mint:", e)
    client.mint_coin(a1.address, 100, auth_key_prefix=a1.auth_key_prefix, is_blocking=True)
    assert 100 == client.get_balance(a1.address)

def test_transfer_coin():
    a1, a2 = create_accounts(2)
    client = create_client()

    try:
        client.transfer_coin(a1, a2.address, 100, is_blocking=True)
        assert 0
    except LibraError as e:
        print("Transfer:", e)
    client.mint_coin(a1.address, 100, auth_key_prefix=a1.auth_key_prefix, is_blocking=True)

    try:
        client.transfer_coin(a1, a2.address, 10, is_blocking=True)
        assert 0
    except LibraError as e:
        print("Transfer:", e)

    try:
        client.transfer_coin(a1, a2.address, 100, is_blocking=True)
        assert 0
    except LibraError as e:
        print("Transfer:", e)

    client.transfer_coin(a1, a2.address, 10, auth_key_prefix=a2.auth_key_prefix, is_blocking=True)
    assert 90 == client.get_balance(a1.address)
    assert 10 == client.get_balance(a2.address)

def test_get_account_state():
    [a1] = create_accounts(1)
    [a2] = create_accounts_with_coins(1)
    client = create_client()
    state = client.get_account_state(a1.address)
    assert None == state
    state = client.get_account_state(a2.address)
    assert isinstance(state, AccountState)

def test_get_account_transaction():
    a1, a2 = create_accounts_with_coins(2)
    client = create_client()
    tx = client.get_account_transaction(a1.address, 0, True)
    assert tx is None
    tx = client.get_account_transaction(association_address(), 1, True)
    assert isinstance(tx, TransactionView)

def test_get_transactions():
    client = create_client()
    version = client.get_latest_version()
    txs = client.get_transactions(version-10, 100, True)
    for tx in txs:
        assert isinstance(tx, TransactionView)

    txs = client.get_transactions(version+10000, 10, True)
    assert len(txs) == 0

def test_get_transaction():
    client = create_client()
    version = client.get_latest_version()
    tx = client.get_transaction(version + 10000, True)
    assert None == tx
    tx = client.get_transaction(version, True)
    assert isinstance(tx, TransactionView)

def test_get_event():
    [a1, a2] = create_accounts_with_coins(2)
    client = create_client()
    client.transfer_coin(a1, a2.address, 10, is_blocking=True)
    client.transfer_coin(a1, a2.address, 10, is_blocking=True)
    events = client.get_sent_events(a1.address, 0, 10)
    assert len(events) == 2
    for event in events:
        assert isinstance(event, EventView)

    events = client.get_received_events(a2.address, 0, 10)
    assert len(events) == 3
    for event in events:
        assert isinstance(event, EventView)

    events = client.get_sent_events(a1.address, 10, 10)
    assert len(events) == 0

    events = client.get_received_events(a2.address, 10, 10)
    assert len(events) == 0

    [a3] = create_accounts(1)
    events = client.get_sent_events(a3.address, 10, 10)
    assert len(events) == 0
    events = client.get_received_events(a3.address, 10, 10)
    assert len(events) == 0

