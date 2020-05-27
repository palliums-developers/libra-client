from uniswap_client import Wallet, Client

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
    client.publish_exchange(module_account)
    client.set_exchange_module_addres(module_account.address)
    client.initialize(module_account)
    resource = client.get_account_state(module_account.address).get_exchange_info_resource()
    assert resource is not None

def test_publish_reserve():
    wallet = Wallet.new()
    client = Client()
    module_account = wallet.new_account()
    client.mint_coin(module_account.address, 10_000_000, auth_key_prefix=module_account.auth_key_prefix,
                     is_blocking=True)
    client.publish_exchange(module_account)
    client.set_exchange_module_addres(module_account.address)
    client.initialize(module_account)
    client.publish_reserve(module_account, "Coin1")
    resource = client.get_account_state(module_account.address).get_reserve_resource("Coin1")
    assert resource is not None

def test_add_liquidity():
    wallet = Wallet.new()
    client = Client()
    module_account = wallet.new_account()
    client.mint_coin(module_account.address, 10_000_000, auth_key_prefix=module_account.auth_key_prefix,
                     is_blocking=True)
    client.publish_exchange(module_account)
    client.set_exchange_module_addres(module_account.address)
    client.initialize(module_account)
    client.publish_reserve(module_account, "Coin1")

    liquidity_account = wallet.new_account()
    client.mint_coin(liquidity_account.address, 10_000_000, auth_key_prefix=liquidity_account.auth_key_prefix,
                     is_blocking=True)
    client.add_currency_to_account(liquidity_account, "Coin1")
    client.mint_coin(liquidity_account.address, 10_000_000, module_name="Coin1", auth_key_prefix=liquidity_account.auth_key_prefix,
                     is_blocking=True)
    client.add_liquidity(liquidity_account, 1, 1_000_000, 1_000_000, "Coin1")

    coin1_balance = client.get_balance(liquidity_account.address, "Coin1")
    lbr_balance = client.get_balance(liquidity_account.address)
    assert coin1_balance == 10_000_000 - 1_000_000
    assert lbr_balance == 10_000_000 - 1_000_000
    resource = client.get_account_state(module_account.address).get_reserve_resource("Coin1")
    assert 1_000_000 == resource.get_token_amount()
    assert 1_000_000 == resource.get_violas_amount()
    assert 1_000_000 == resource.get_liquidity_total_supply()


def test_remove_liquidity():
    wallet = Wallet.new()
    client = Client()
    module_account = wallet.new_account()
    client.mint_coin(module_account.address, 10_000_000, auth_key_prefix=module_account.auth_key_prefix,
                     is_blocking=True)
    client.publish_exchange(module_account)
    client.set_exchange_module_addres(module_account.address)
    client.initialize(module_account)
    client.publish_reserve(module_account, "Coin1")

    liquidity_account = wallet.new_account()
    client.mint_coin(liquidity_account.address, 10_000_000, auth_key_prefix=liquidity_account.auth_key_prefix,
                     is_blocking=True)
    client.add_currency_to_account(liquidity_account, "Coin1")
    client.mint_coin(liquidity_account.address, 10_000_000, module_name="Coin1", auth_key_prefix=liquidity_account.auth_key_prefix,
                     is_blocking=True)
    client.add_liquidity(liquidity_account, 1, 1_000_000, 1_000_000, "Coin1")
    client.remove_liquidity(liquidity_account, 500_000, 1, 1, "Coin1", exchange_module_address=module_account.address)
    coin1_balance = client.get_balance(liquidity_account.address, "Coin1")
    lbr_balance = client.get_balance(liquidity_account.address)
    assert coin1_balance == 10_000_000 - 500_000
    assert lbr_balance == 10_000_000 - 500_000
    resource = client.get_account_state(module_account.address).get_reserve_resource("Coin1")
    assert 500_000 == resource.get_token_amount()
    assert 500_000 == resource.get_violas_amount()
    assert 500_000 == resource.get_liquidity_total_supply()

def test_violas_to_token_swap():
    wallet = Wallet.new()
    client = Client()
    module_account = wallet.new_account()
    client.mint_coin(module_account.address, 10_000_000, auth_key_prefix=module_account.auth_key_prefix,
                     is_blocking=True)
    client.publish_exchange(module_account)
    client.set_exchange_module_addres(module_account.address)
    client.initialize(module_account)
    client.publish_reserve(module_account, "Coin1")

    liquidity_account = wallet.new_account()
    client.mint_coin(liquidity_account.address, 10_000_000, auth_key_prefix=liquidity_account.auth_key_prefix,
                     is_blocking=True)
    client.add_currency_to_account(liquidity_account, "Coin1")
    client.mint_coin(liquidity_account.address, 10_000_000, module_name="Coin1", auth_key_prefix=liquidity_account.auth_key_prefix,
                     is_blocking=True)
    client.add_liquidity(liquidity_account, 1, 1_000_000, 1_000_000, "Coin1")
    swap_account = liquidity_account
    violas_balance = client.get_balance(swap_account.address)
    token_blance = client.get_balance(swap_account.address, "Coin1")
    input = swap_output(10_000, 1_000_000, 1_000_000)
    client.violas_to_token_swap(swap_account, input, 1, "Coin1", exchange_module_address=module_account.address)
    assert client.get_balance(swap_account.address) == violas_balance - input
    assert client.get_balance(swap_account.address, "Coin1") == token_blance + 10_000

def test_token_to_violas_swap():
    wallet = Wallet.new()
    client = Client()
    module_account = wallet.new_account()
    client.mint_coin(module_account.address, 10_000_000, auth_key_prefix=module_account.auth_key_prefix,
                     is_blocking=True)
    client.publish_exchange(module_account)
    client.set_exchange_module_addres(module_account.address)
    client.initialize(module_account)
    client.publish_reserve(module_account, "Coin1")

    liquidity_account = wallet.new_account()
    client.mint_coin(liquidity_account.address, 10_000_000, auth_key_prefix=liquidity_account.auth_key_prefix,
                     is_blocking=True)
    client.add_currency_to_account(liquidity_account, "Coin1")
    client.mint_coin(liquidity_account.address, 10_000_000, module_name="Coin1", auth_key_prefix=liquidity_account.auth_key_prefix,
                     is_blocking=True)
    client.add_liquidity(liquidity_account, 1, 1_000_000, 1_000_000, "Coin1")
    swap_account = liquidity_account
    violas_balance = client.get_balance(swap_account.address)
    token_blance = client.get_balance(swap_account.address, "Coin1")
    input = swap_output(10_000, 1_000_000, 1_000_000)
    client.token_to_violas_swap(swap_account, input, 1, "Coin1", exchange_module_address=module_account.address)
    assert client.get_balance(swap_account.address, "Coin1") == token_blance - input
    assert client.get_balance(swap_account.address) == violas_balance + 10_000

def test_token_to_token_swap():
    wallet = Wallet.new()
    client = Client()
    module_account = wallet.new_account()
    client.mint_coin(module_account.address, 10_000_000, auth_key_prefix=module_account.auth_key_prefix,
                     is_blocking=True)
    client.publish_exchange(module_account)
    client.set_exchange_module_addres(module_account.address)
    client.initialize(module_account)
    client.publish_reserve(module_account, "Coin1")
    client.publish_reserve(module_account, "Coin2")

    liquidity_account = wallet.new_account()
    swap_account = wallet.new_account()
    client.mint_coin(liquidity_account.address, 10_000_000, auth_key_prefix=liquidity_account.auth_key_prefix,
                     is_blocking=True)
    client.mint_coin(swap_account.address, 10_000_000, auth_key_prefix=swap_account.auth_key_prefix,
                     is_blocking=True)

    client.add_currency_to_account(liquidity_account, "Coin1")
    client.add_currency_to_account(liquidity_account, "Coin2")
    client.add_currency_to_account(swap_account, "Coin1")
    client.add_currency_to_account(swap_account, "Coin2")


    client.mint_coin(liquidity_account.address, 10_000_000, module_name="Coin1", auth_key_prefix=liquidity_account.auth_key_prefix,
                     is_blocking=True)
    client.mint_coin(liquidity_account.address, 10_000_000, module_name="Coin2", auth_key_prefix=liquidity_account.auth_key_prefix,
                     is_blocking=True)

    client.mint_coin(swap_account.address, 10_000_000, module_name="Coin1", auth_key_prefix=swap_account.auth_key_prefix,
                     is_blocking=True)
    client.mint_coin(swap_account.address, 10_000_000, module_name="Coin2", auth_key_prefix=swap_account.auth_key_prefix,
                     is_blocking=True)

    client.add_liquidity(liquidity_account, 1, 1_000_000, 1_000_000, "Coin1")
    client.add_liquidity(liquidity_account, 1, 1_000_000, 1_000_000, "Coin2")

    output = 100_000
    input = swap_output(output, 1_000_000, 1_000_000)
    input = swap_output(input, 1_000_000, 1_000_000)

    client.token_to_token_swap(swap_account, tokens_sold=input, min_tokens_bought=output, min_violas_bought=1, sold_token_module_name="Coin1", bought_token_module_name="Coin2")
    assert client.get_balance(swap_account.address, "Coin1") == 10_000_000 - input
    assert client.get_balance(swap_account.address, "Coin2") == 10_000_000 + output

def test_client():
    wallet = Wallet.new()
    client = Client()
    a1 = wallet.new_account()
    a2 = wallet.new_account()

    module_account = wallet.new_account()
    client.mint_coin(a1.address, 10_000_000, auth_key_prefix=a1.auth_key_prefix, is_blocking=True)
    client.mint_coin(a2.address, 10_000_000, auth_key_prefix=a2.auth_key_prefix, is_blocking=True)
    client.mint_coin(module_account.address, 10_000_000, auth_key_prefix=module_account.auth_key_prefix,
                     is_blocking=True)

    client.add_currency_to_account(a1, "Coin1")
    client.add_currency_to_account(a2, "Coin1")
    client.add_currency_to_account(a1, "Coin2")
    client.add_currency_to_account(a2, "Coin2")
    client.mint_coin(a1.address, 10_000_000, module_name="Coin1")
    client.mint_coin(a2.address, 10_000_000, module_name="Coin1")
    client.mint_coin(a1.address, 10_000_000, module_name="Coin2")
    client.mint_coin(a2.address, 10_000_000, module_name="Coin2")
    client.publish_exchange(module_account)
    client.set_exchange_module_addres(module_account.address)
    client.initialize(module_account)
    client.publish_reserve(module_account, "Coin1")
    client.publish_reserve(module_account, "Coin2")
    client.add_liquidity(a1, 100_000, 200_000, 200_000, "Coin1", exchange_module_address=module_account.address)
    client.add_liquidity(a1, 100_000, 200_000, 200_000, "Coin2", exchange_module_address=module_account.address)
    client.token_to_token_swap(sender_account=a1, tokens_sold=100, min_tokens_bought=10, min_violas_bought=10,
                               sold_token_module_name="Coin1", bought_token_module_name="Coin2")

    client.violas_to_token_swap(sender_account=a1, violas_sold=100, min_tokens=10, token_module_name="Coin1", exchange_module_address=module_account.address)
    client.token_to_violas_swap(sender_account=a1, tokens_sold=100, min_violas=10, token_module_name="Coin1", exchange_module_address=module_account.address)

