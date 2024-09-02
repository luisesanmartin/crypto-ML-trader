import robin_stocks.robinhood as robinhood
import robin_stocks.robinhood.orders as rh
import json

def login():

    '''
    Logs in
    '''

    with open('API/credentials.json') as f:
        login_info = json.load(f)

    login = robinhood.login(login_info['username'], login_info['password'])

    return login

def buy_crypto(crypto, usd_amount):

    '''
    Buys the specified amount of dollars of crypto
    '''

    order = rh.order_buy_crypto_by_price(crypto, usd_amount)

    return order

def buy_crypto_limit(crypto, usd_amount, limit_price):

    '''
    Buys the specified amount of dollars of crypto, with a limit price
    '''

    order = rh.order_buy_crypto_limit_by_price(crypto, usd_amount, limit_price)

    return order

def sell_crypto(crypto, crypto_amount):

    '''
    Sells the specified amount of crypto at the current price
    '''

    order = rh.order_sell_crypto_by_quantity(crypto, crypto_amount)

    return order

def sell_crypto_limit(crypto, crypto_amount, limit_price):

    '''
    Sells the specified amount of crypto with a limit price
    '''

    order = rh.order_sell_crypto_limit(crypto, crypto_amount, limit_price)

    return order
