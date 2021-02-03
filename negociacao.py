from urllib.parse import urlencode
import hashlib
import hmac

# Constantes e Parâmetros
# Do exemplo acima, '1ebda7d457ece1330dff1c9e04cd62c4e02d1835968ff89d2fb2339f06f73028'

import json

def get_tapi_secreto():
    with open("chave_secreta.json", 'r', encoding='utf-8' ) as infile:
        texto = infile.read()
        y = json.loads(texto)
        return y["identificador"], y["segredo"]


REQUEST_PATH = '/tapi/v3/'





import hashlib
import hmac
import json

from http import client
from urllib.parse import urlencode


# Constantes
MB_TAPI_ID, MB_TAPI_SECRET = get_tapi_secreto()
REQUEST_HOST = 'www.mercadobitcoin.net'
REQUEST_PATH = '/tapi/v3/'

# Nonce
# Para obter variação de forma simples
# timestamp pode ser utilizado:
import time
tapi_nonce = str(int(time.time()))

# tapi_nonce = 1


def conectar(params, response_func):
    params = urlencode(params)

    # Gerar MAC
    params_string = REQUEST_PATH + '?' + params
    H = hmac.new(bytes(MB_TAPI_SECRET, encoding='utf8'), digestmod=hashlib.sha512)
    H.update(params_string.encode('utf-8'))
    tapi_mac = H.hexdigest()

    # Gerar cabeçalho da requisição
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'TAPI-ID': MB_TAPI_ID,
        'TAPI-MAC': tapi_mac
    }

    # Realizar requisição POST
    try:
        conn = client.HTTPSConnection(REQUEST_HOST)
        conn.request("POST", REQUEST_PATH, params, headers)

        # Print response data to console
        response = conn.getresponse()
        response = response.read()

        response_json = json.loads(response)
        response_func(response_json)
    finally:
        if conn:
            conn.close()

def mostra_tela_resultado(response_json):
    print('status: {}'.format(response_json['status_code']))
    print(json.dumps(response_json, indent=4))


def get_account_info():
    tapi_nonce = str(int(time.time()))
    params = {
    'tapi_method': 'get_account_info',
    'tapi_nonce': tapi_nonce}
    conectar(params,mostra_tela_resultado)

def get_list_order(coin_pair="XRP"):
    tapi_nonce = str(int(time.time()))
    params = {
    'tapi_method': 'list_orders',
    'tapi_nonce': tapi_nonce,
    'coin_pair':  f'BRL{coin_pair}',}

    conectar(params,mostra_tela_resultado)


def place_buy_order(price: str, quantity="0.1", coin_pair="XRP", fnc_retorno = None):
    tapi_nonce = str(int(time.time()))
    params = {
    'tapi_method': 'place_buy_order',
    'tapi_nonce': tapi_nonce,
    'coin_pair': f'BRL{coin_pair}',
    "quantity":  quantity, # LTC: 0.01, XRP: 0.1
    "limit_price": price}
    if fnc_retorno == None:
        conectar(params,mostra_tela_resultado)
    else:
        conectar(params,fnc_retorno)

def get_order(order_id, coin_pair="XRP", fnc_retorno = None):
    tapi_nonce = str(int(time.time()))
    params = {
    'tapi_method': 'get_order',
    'tapi_nonce': tapi_nonce,
    'coin_pair': f'BRL{coin_pair}',
    'order_id': int(order_id)}
    
    if fnc_retorno == None:
        conectar(params,mostra_tela_resultado)
    else:
        conectar(params,fnc_retorno)



def place_sell_order(price: str, quantity="0.1", coin_pair="XRP", fnc_retorno = None):
    tapi_nonce = str(int(time.time()))
    params = {
    'tapi_method': 'place_sell_order',
    'tapi_nonce': tapi_nonce,
    'coin_pair': f'BRL{coin_pair}',
    "quantity":  quantity,
    "limit_price": price}

    if fnc_retorno == None:
        conectar(params,mostra_tela_resultado)
    else:
        conectar(params,fnc_retorno)


def list_orderbook(coin_pair="XRP", fnc_retorno= None):
    tapi_nonce = str(int(time.time()))
    params = {
    'tapi_method': 'list_orderbook',
    'tapi_nonce': tapi_nonce,
    'coin_pair': f'BRL{coin_pair}'
    }

    if fnc_retorno == None:
        conectar(params,mostra_tela_resultado)
    else:
        conectar(params,fnc_retorno)

def cancel_order(order_id, coin_pair="XRP"):
    tapi_nonce = str(int(time.time()))
    params = {'tapi_method': 'cancel_order',
        'tapi_nonce': tapi_nonce,
        "coin_pair": f'BRL{coin_pair}',
        "order_id": order_id }
    
    conectar(params,mostra_tela_resultado)