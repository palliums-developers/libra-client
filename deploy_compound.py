from violas_client import Client, Wallet

def publish_compound_module():
    wallet = Wallet.new()
    a1 = wallet.new_account()
    client = Client("bj_testnet")
    client.mint_coin(a1.address, 50_000_000, auth_key_prefix=a1.auth_key_prefix, gas_currency_code="USD")
    client.bank_publish_module(a1)
    client.set_bank_module_address(a1.address)
    client.set_bank_owner_address(a1.address)
    client.bank_publish(a1)
    client.bank_register_token(a1, "USD", a1.address, collater_factor=0.5, base_rate=0.15, rate_multiplier=0.2, rate_jump_mutiplier=0.4, rate_kink=0.8)
    return a1.address

if __name__ == "__main__":
    publish_compound_module()