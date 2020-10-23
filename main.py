from violas_client import Client, Wallet




client = Client()
wallet = Wallet.new()
a1 = wallet.new_account()
a2 = wallet.new_account()
amount = client.bank_get_amounts(client.testnet_dd_account.address)
print(amount)

# client.tiered_mint(9**15, currency_code="USD")
# print(client.get_balance(client.testnet_dd_account.address, "USD"))


# client.mint_coin(a1.address, 1_000_000_000, auth_key_prefix=a1.auth_key_prefix, currency_code="USD")
# client.mint_coin(a2.address, 30_000_000_000, auth_key_prefix=a2.auth_key_prefix, currency_code="EUR")
# client.rotate_dual_attestation_info(a1, new_url="url")
# client.rotate_dual_attestation_info(a2, new_url="url")

# metadata = b"0"
# amount = 10_000_000_000
# m = metadata
# m += Message(bytes.fromhex("2e9829f376318154bff603ebc8e0b743"), amount).serialize()
# m += b"@@$$LIBRA_ATTEST$$@@"
# print(m.hex())
# sig = a2.sign(m)[:64]
#
# client.transfer_coin(a1, a2.address, amount, currency_code="EUR", data=metadata, metadata_signature=sig)
# client.rotate_dual_attestation_info(a1, "new_url")

# print(a1.address_hex)
