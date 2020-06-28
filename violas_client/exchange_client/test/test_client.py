from exchange_client import Wallet, Client

def swap_input(input_amount, input_reserve, output_reserve):
    input_amount_with_fee = input_amount * 997
    numerator = input_amount_with_fee * output_reserve
    denominator = input_reserve * 1000 + input_amount_with_fee
    return numerator // denominator

def swap_output(output_amount, input_reserve, output_reserve):
    numerator = input_reserve * output_amount * 1000
    denominator = (output_reserve - output_amount) * 997
    return numerator // denominator + 1


def mint_liquity_token(violas_input, total_liquidity, token_reserve, violas_reserve) -> (int, int):
    if total_liquidity > 0:
        liquidity_minted = violas_input * total_liquidity // violas_reserve
        token_amount = violas_input * token_reserve // violas_reserve + 1
    else:
        liquidity_minted = violas_input
        token_amount = 10000000
    return (int(liquidity_minted), int(token_amount))

def test_initilaize():
    wallet = Wallet.new()
    client = Client()
    module_account = wallet.new_account()
    client.mint_coin(module_account.address, 10_000_000, auth_key_prefix=module_account.auth_key_prefix,
                     is_blocking=True)
    client.swap_publish_contract(module_account)
    client.set_exchange_module_address(module_account.address)
    client.swap_initialize(module_account)
    resource = client.swap_get_account_state(module_account.address).swap_get_reserves_resource()
    assert resource is not None

def test_publish_reserve():
    wallet = Wallet.new()
    client = Client()
    module_account = wallet.new_account()
    client.mint_coin(module_account.address, 10_000_000, auth_key_prefix=module_account.auth_key_prefix,
                     is_blocking=True)
    client.swap_publish_contract(module_account)
    client.set_exchange_module_address(module_account.address)
    client.swap_initialize(module_account)
    client.swap_add_currency(module_account, "Coin1")
    resource = client.swap_get_account_state(module_account.address).swap_get_balance("Coin1")
    assert resource is not None

def test_add_liquidity():
    wallet = Wallet.new()
    client = Client()
    module_account = wallet.new_account()
    client.mint_coin(module_account.address, 10_000_000, auth_key_prefix=module_account.auth_key_prefix,
                     is_blocking=True)
    client.swap_publish_contract(module_account)
    client.set_exchange_module_address(module_account.address)
    client.swap_initialize(module_account)
    client.swap_add_currency(module_account, "LBR")
    client.swap_add_currency(module_account, "Coin1")

    liquidity_account = wallet.new_account()
    client.mint_coin(liquidity_account.address, 10_000_000, auth_key_prefix=liquidity_account.auth_key_prefix,
                     is_blocking=True)
    client.add_currency_to_account(liquidity_account, "Coin1")
    client.mint_coin(liquidity_account.address, 10_000_000, currency_code="Coin1", auth_key_prefix=liquidity_account.auth_key_prefix,
                     is_blocking=True)

    swap_account = wallet.new_account()
    client.mint_coin(swap_account.address, 10_000_000, auth_key_prefix=swap_account.auth_key_prefix,
                     is_blocking=True)
    client.add_currency_to_account(swap_account, "Coin1")
    client.mint_coin(swap_account.address, 10_000_000, currency_code="Coin1", auth_key_prefix=swap_account.auth_key_prefix,
                     is_blocking=True)

    lbr_before_balance = client.get_balance(liquidity_account.address, "LBR")
    coin1_before_balance = client.get_balance(liquidity_account.address, "Coin1")
    client.swap_add_liquidity(liquidity_account, "LBR", "Coin1", 1_000_000, 321_432)
    lbr_after_balance = client.get_balance(liquidity_account.address, "LBR")
    coin1_after_balance = client.get_balance(liquidity_account.address, "Coin1")
    assert lbr_before_balance - lbr_after_balance == 1_000_000
    assert coin1_before_balance - coin1_after_balance == 321_432
    liquidity_balance = client.swap_get_liquidity_balances(liquidity_account.address)
    assert liquidity_balance[0]["liquidity"] == int((1_000_000*321_432)**0.5)

def test_remove_liquidity():
    wallet = Wallet.new()
    client = Client()
    module_account = wallet.new_account()
    client.mint_coin(module_account.address, 10_000_000, auth_key_prefix=module_account.auth_key_prefix,
                     is_blocking=True)
    client.swap_publish_contract(module_account)
    client.set_exchange_module_address(module_account.address)
    client.swap_initialize(module_account)
    client.swap_add_currency(module_account, "LBR")
    client.swap_add_currency(module_account, "Coin1")

    liquidity_account = wallet.new_account()
    client.mint_coin(liquidity_account.address, 10_000_000, auth_key_prefix=liquidity_account.auth_key_prefix,
                     is_blocking=True)
    client.add_currency_to_account(liquidity_account, "Coin1")
    client.mint_coin(liquidity_account.address, 10_000_000, currency_code="Coin1",
                     auth_key_prefix=liquidity_account.auth_key_prefix,
                     is_blocking=True)

    swap_account = wallet.new_account()
    client.mint_coin(swap_account.address, 10_000_000, auth_key_prefix=swap_account.auth_key_prefix,
                     is_blocking=True)
    client.add_currency_to_account(swap_account, "Coin1")
    client.mint_coin(swap_account.address, 10_000_000, currency_code="Coin1",
                     auth_key_prefix=swap_account.auth_key_prefix,
                     is_blocking=True)

    client.swap_add_liquidity(liquidity_account, "LBR", "Coin1", 1_000_000, 321_432)
    client.swap_remove_liquidity(liquidity_account, "Coin1", "LBR", int((1_000_000 * 321_432) ** 0.5), amounta_min=321_432, amountb_min=1_000_000)

def test_swap():
    wallet = Wallet.new()
    client = Client()
    module_account = wallet.new_account()
    client.mint_coin(module_account.address, 10_000_000, auth_key_prefix=module_account.auth_key_prefix,
                     is_blocking=True)
    client.swap_publish_contract(module_account)
    client.set_exchange_module_address(module_account.address)
    client.swap_initialize(module_account)
    client.swap_add_currency(module_account, "LBR")
    client.swap_add_currency(module_account, "Coin1")
    client.swap_add_currency(module_account, "Coin2")


    liquidity_account = wallet.new_account()
    client.mint_coin(liquidity_account.address, 10_000_000, auth_key_prefix=liquidity_account.auth_key_prefix,
                     is_blocking=True)
    client.add_currency_to_account(liquidity_account, "Coin1")
    client.mint_coin(liquidity_account.address, 10_000_000, currency_code="Coin1",
                     auth_key_prefix=liquidity_account.auth_key_prefix,
                     is_blocking=True)
    client.add_currency_to_account(liquidity_account, "Coin2")
    client.mint_coin(liquidity_account.address, 10_000_000, currency_code="Coin2",
                     auth_key_prefix=liquidity_account.auth_key_prefix,
                     is_blocking=True)

    swap_account = wallet.new_account()
    client.mint_coin(swap_account.address, 10_000_000, auth_key_prefix=swap_account.auth_key_prefix,
                     is_blocking=True)
    client.add_currency_to_account(swap_account, "Coin1")
    client.mint_coin(swap_account.address, 10_000_000, currency_code="Coin1",
                     auth_key_prefix=swap_account.auth_key_prefix,
                     is_blocking=True)
    client.add_currency_to_account(swap_account, "Coin2")
    client.mint_coin(swap_account.address, 10_000_000, currency_code="Coin2",
                     auth_key_prefix=swap_account.auth_key_prefix,
                     is_blocking=True)

    client.swap_add_liquidity(liquidity_account, "LBR", "Coin1", 123_321, 321_432)
    client.swap_add_liquidity(liquidity_account, "Coin2", "Coin1", 321_432, 321_432)

    expected_amount = client.swap_get_expected_swap_amount("Coin1", "LBR", 1000)
    before_amount = client.get_balance(swap_account.address, "LBR")
    client.swap(swap_account, "Coin1", "LBR", 1000, expected_amount)
    after_amount = client.get_balance(swap_account.address, "LBR")
    assert after_amount - before_amount == expected_amount

def test_get_expected_swap_amount():
    wallet = Wallet.new()
    client = Client()
    module_account = wallet.new_account()
    client.mint_coin(module_account.address, 10_000_000, auth_key_prefix=module_account.auth_key_prefix,
                     is_blocking=True)
    client.swap_publish_contract(module_account)
    client.set_exchange_module_address(module_account.address)
    client.swap_initialize(module_account)
    client.swap_add_currency(module_account, "LBR")
    client.swap_add_currency(module_account, "Coin1")
    client.swap_add_currency(module_account, "Coin2")

    liquidity_account = wallet.new_account()
    client.mint_coin(liquidity_account.address, 10_000_000, auth_key_prefix=liquidity_account.auth_key_prefix,
                     is_blocking=True)
    client.add_currency_to_account(liquidity_account, "Coin1")
    client.mint_coin(liquidity_account.address, 10_000_000, currency_code="Coin1",
                     auth_key_prefix=liquidity_account.auth_key_prefix,
                     is_blocking=True)
    client.add_currency_to_account(liquidity_account, "Coin2")
    client.mint_coin(liquidity_account.address, 10_000_000, currency_code="Coin2",
                     auth_key_prefix=liquidity_account.auth_key_prefix,
                     is_blocking=True)

    swap_account = wallet.new_account()
    client.mint_coin(swap_account.address, 10_000_000, auth_key_prefix=swap_account.auth_key_prefix,
                     is_blocking=True)
    client.add_currency_to_account(swap_account, "Coin1")
    client.mint_coin(swap_account.address, 10_000_000, currency_code="Coin1",
                     auth_key_prefix=swap_account.auth_key_prefix,
                     is_blocking=True)
    client.add_currency_to_account(swap_account, "Coin2")
    client.mint_coin(swap_account.address, 10_000_000, currency_code="Coin2",
                     auth_key_prefix=swap_account.auth_key_prefix,
                     is_blocking=True)

    client.swap_add_liquidity(liquidity_account, "LBR", "Coin1", 200_000, 100_000)
    client.swap_add_liquidity(liquidity_account, "Coin2", "Coin1", 100_000, 200_000)
    expected_amount = client.swap_get_expected_swap_amount("Coin2", "LBR", 100)
    client.swap(swap_account, "Coin2", "LBR", 100)
    assert client.get_balance(swap_account.address, "LBR") == 10_000_000 + expected_amount

def test_get_liquidity_balances():
    wallet = Wallet.new()
    client = Client()
    module_account = wallet.new_account()
    client.mint_coin(module_account.address, 10_000_000, auth_key_prefix=module_account.auth_key_prefix,
                     is_blocking=True)
    client.swap_publish_contract(module_account)
    client.set_exchange_module_address(module_account.address)
    client.swap_initialize(module_account)
    client.swap_add_currency(module_account, "LBR")
    client.swap_add_currency(module_account, "Coin1")
    client.swap_add_currency(module_account, "Coin2")

    liquidity_account = wallet.new_account()
    client.mint_coin(liquidity_account.address, 10_000_000, auth_key_prefix=liquidity_account.auth_key_prefix,
                     is_blocking=True)
    client.add_currency_to_account(liquidity_account, "Coin1")
    client.mint_coin(liquidity_account.address, 10_000_000, currency_code="Coin1",
                     auth_key_prefix=liquidity_account.auth_key_prefix,
                     is_blocking=True)
    client.add_currency_to_account(liquidity_account, "Coin2")
    client.mint_coin(liquidity_account.address, 10_000_000, currency_code="Coin2",
                     auth_key_prefix=liquidity_account.auth_key_prefix,
                     is_blocking=True)

    swap_account = wallet.new_account()
    client.mint_coin(swap_account.address, 10_000_000, auth_key_prefix=swap_account.auth_key_prefix,
                     is_blocking=True)
    client.add_currency_to_account(swap_account, "Coin1")
    client.mint_coin(swap_account.address, 10_000_000, currency_code="Coin1",
                     auth_key_prefix=swap_account.auth_key_prefix,
                     is_blocking=True)
    client.add_currency_to_account(swap_account, "Coin2")
    client.mint_coin(swap_account.address, 10_000_000, currency_code="Coin2",
                     auth_key_prefix=swap_account.auth_key_prefix,
                     is_blocking=True)

    client.swap_add_liquidity(liquidity_account, "LBR", "Coin1", 200_000, 100_000)
    client.swap(swap_account, "Coin1", "LBR", 100_000)
    liquidity_balance = client.swap_get_liquidity_balances(liquidity_account.address)
    client.swap_remove_liquidity(liquidity_account, "Coin1", "LBR", liquidity_balance[0]["liquidity"])
    assert client.get_balance(liquidity_account.address, "LBR") == 10_000_000 - 200_000 + liquidity_balance[0]["LBR"]
    assert client.get_balance(liquidity_account.address, "Coin1") == 10_000_000 - 100_000 + liquidity_balance[0]["Coin1"]
    assert client.swap_get_reserves_resource()[0].liquidity_total_supply == 0


def test_get_expected_liquidity_amount():
    wallet = Wallet.new()
    client = Client()
    module_account = wallet.new_account()
    client.mint_coin(module_account.address, 10_000_000, auth_key_prefix=module_account.auth_key_prefix,
                     is_blocking=True)
    client.swap_publish_contract(module_account)
    client.set_exchange_module_address(module_account.address)
    client.swap_initialize(module_account)
    client.swap_add_currency(module_account, "LBR")
    client.swap_add_currency(module_account, "Coin1")
    client.swap_add_currency(module_account, "Coin2")

    liquidity_account = wallet.new_account()
    client.mint_coin(liquidity_account.address, 10_000_000, auth_key_prefix=liquidity_account.auth_key_prefix,
                     is_blocking=True)
    client.add_currency_to_account(liquidity_account, "Coin1")
    client.mint_coin(liquidity_account.address, 10_000_000, currency_code="Coin1",
                     auth_key_prefix=liquidity_account.auth_key_prefix,
                     is_blocking=True)
    client.add_currency_to_account(liquidity_account, "Coin2")
    client.mint_coin(liquidity_account.address, 10_000_000, currency_code="Coin2",
                     auth_key_prefix=liquidity_account.auth_key_prefix,
                     is_blocking=True)

    swap_account = wallet.new_account()
    client.mint_coin(swap_account.address, 10_000_000, auth_key_prefix=swap_account.auth_key_prefix,
                     is_blocking=True)
    client.add_currency_to_account(swap_account, "Coin1")
    client.mint_coin(swap_account.address, 10_000_000, currency_code="Coin1",
                     auth_key_prefix=swap_account.auth_key_prefix,
                     is_blocking=True)
    client.add_currency_to_account(swap_account, "Coin2")
    client.mint_coin(swap_account.address, 10_000_000, currency_code="Coin2",
                     auth_key_prefix=swap_account.auth_key_prefix,
                     is_blocking=True)

    client.swap_add_liquidity(liquidity_account, "LBR", "Coin1", 200_000, 100_000)
    expected_amount = client.swap_get_expected_liquidity_amount("Coin1", "LBR", 100)
    client.swap_add_liquidity(liquidity_account, "Coin1", "LBR", 100, 100_000)
    assert client.get_balance(liquidity_account.address, "LBR") == 10_000_000 - 200_000 - expected_amount









