from libra_client import Client
from libra.account_config import AccountConfig
from canoser import StrT
address = AccountConfig.association_address()
from libra_client import Wallet
from libra.transaction import Script, TransactionPayload, SignedTransaction
from json_rpc.views import EventView, TransactionView
from test import create_accounts, create_client, create_accounts_with_coins

[a1, a2] = create_accounts_with_coins(2)
client = create_client()
client.transfer_coins(a1, 10, a2.address, is_blocking=True)
client.transfer_coins(a1, 10, a2.address, is_blocking=True)
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
