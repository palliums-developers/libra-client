from libra_client import Client, Wallet


client = Client()
wallet = Wallet.new()
code = "charge vacuum raccoon demand smart jacket unit spare poverty hero ordinary ball pudding law puzzle party crucial accident aerobic dad diagram desert green spike"
code = "cost oppose sense coyote cup spider hedgehog always catch total badge focus cable million fringe hello exhaust unfair dragon amazing local buzz noise ocean"
v = Wallet.new_from_mnemonic(code)
print(v.new_account().address_hex)


