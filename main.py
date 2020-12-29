from violas_client import Client, Wallet
import time
from enum import IntEnum
from violas_client.extypes.bytecode import CodeType as ExchangeType

wallet = Wallet.new()
client = Client()
txs = client.get_transactions(23924000, 500)


