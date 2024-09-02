import objects
import json
import requests

def get_api_key(text='API/key.txt'):

    with open(text) as file:
        key = file.read()

    return key

def get_data_min(period=objects.PERIOD_DATA, crypto_symbol=objects.SYMBOL_ID):

    '''
    Retrieves data for a crypto, with a frequency of 'period'
    '''

    request_url = objects.URL.format(crypto_symbol)
    headers = {"X-CoinAPI-Key": get_api_key()}
    parameters = {'period_id': objects.PERIOD_DATA}

    response = requests.get(request_url, headers=headers, params=parameters)
    data = json.loads(response.text)

    return data
