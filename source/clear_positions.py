import os, sys
import time
from binance.spot import Spot
from trader import get_keys, get_all_assets
from configuration_trading import ETH_ROUND_NUMBER, MARKET
import math

PROJECT_PATH = os.getcwd()
sys.path.append(PROJECT_PATH.replace('minerva/',''))

def cancel_all_open_orders(api_key_, api_secret_):
    """
    Cancels all open orders for a given trading account.

    Arguments:
    - api_key_: API key for the Binance account.
    - api_secret_: API secret for the Binance account.

    Returns:
    - response: Response from the Binance API for canceling the open orders.
    """
    client = Spot(api_key=api_key_, private_key=api_secret_)
    if client.get_open_orders():
        response = client.cancel_open_orders(symbol=TICKER + BASE_CURRENCY)
        print(f"Canceling open orders on {TICKER}")
        return response

def sell_all_tokens(api_key, api_secret):
    """
    Sells all tokens for a given trading account.

    Arguments:
    - api_key: API key for the Binance account.
    - api_secret: API secret for the Binance account.

    Returns:
    - response: Response from the Binance API for placing the sell order.
    """
    client = Spot(api_key=api_key, private_key=api_secret)
    assets = get_all_assets(client=client)

    token_quantity = round(assets[TICKER] * 0.98, ETH_ROUND_NUMBER + 2) 
    if token_quantity:
        params = {
            'symbol': MARKET,
            'side': 'SELL',
            'type': 'MARKET',
            'quantity': token_quantity,
        }
        print(params)
        response = client.new_order(**params)
        print('All tokens are in market sell orders')
        return response
    else:
        print('No tokens found')
        return 0

def reset_account(api_key, api_secret):
    """
    Resets the trading account by canceling open orders and selling all tokens.

    Arguments:
    - api_key: API key for the Binance account.
    - api_secret: API secret for the Binance account.
    """
    cancel_all_open_orders(api_key, api_secret)
    time.sleep(2)
    sell_all_tokens(api_key, api_secret)

if __name__ == "__main__":
    # reset token quantity in USDT
    TICKER = "ETH"
    BASE_CURRENCY = "USDT"
    api_key, private_key = get_keys(name_account="admin1")
    reset_account(api_key, private_key)
