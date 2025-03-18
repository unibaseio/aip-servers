# util.py

import pkgutil
from web3 import Web3 
from web3.contract import Contract

import os
import requests
import json

from typing import Optional

def _load_contract_erc20(w3: Web3, token_address: str) -> Contract:
    contract_abi = pkgutil.get_data('chain', 'solc/Token.abi').decode()
    return w3.eth.contract(address=token_address, abi=contract_abi)


def _create_wallet(app_id: str):
    url = f"https://api.privy.io/v1/wallets/"
    headers = {
        "privy-app-id": app_id,
        "Content-Type": "application/json"
    }

    app_secret = os.getenv('PRIVY_APP_SECRET')
    data = {
        "chain_type": "ethereum"
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), auth=(app_id, app_secret))
        response.raise_for_status()
        print(response.json())
        return response.json()['address'], response.json()['id']
    except Exception as e:
        print(response.json())
        raise e


def _sign_transcation(app_id: str, wallet_id: str, tx: dict):
    url = f"https://api.privy.io/v1/wallets/{wallet_id}/rpc"
    headers = {
        "privy-app-id": app_id,
        "Content-Type": "application/json"
    }

    transcation = {
        'to': tx['to'],
        'nonce': tx['nonce'],
        'gas_limit': tx['gas'],
        'gas_price': tx['gasPrice'],
        'value': tx['value'],
        'chain_id': tx['chainId'],
        'type': 0,
    }

    #print(transcation)

    data = tx.get('data')
    if (data):
         transcation['data'] = data

    app_secret = os.getenv('PRIVY_APP_SECRET')
    data = {
        "method": "eth_signTransaction",
        "params": {
            "transaction": transcation
        }
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), auth=(app_id, app_secret))
        response.raise_for_status()
        return response.json()['data']['signed_transaction']
    except Exception as e:
        print(response.json())
        raise e 
    
def get_0x_quote(
        buy_token: str,
        sell_token: str,
        sell_amount: int,
        taker: str,
        chain_id: str, 
        gas_price: Optional[int] = None,
        slippage: Optional[float] = None,
    ):
        """
        Docs: https://0x.org/docs/api#tag/Swap/operation/swap::permit2::getQuote
        """

        url = "https://api.0x.org/swap/permit2/quote"
        params = {
            'buyToken': buy_token,
            'sellToken': sell_token,
            'sellAmount': sell_amount,
            'chainId': chain_id,
            'taker': taker,
        }

        if gas_price:
            params['gasPrice'] = gas_price

        if slippage:
            params['slippageBps'] = slippage

        print(f'Get url {url} with params {params}')

        headers = {
            "Content-Type": "application/json",
            "0x-api-key": os.getenv('ZEROX_API_KEY', "c9f13c84-9fcb-4f42-aa30-a11b0d016aa5"),
            "0x-version": "v2"
        }

        response = requests.get("https://api.0x.org/swap/permit2/quote", params=params, headers=headers)
        try:
            response.raise_for_status()
            print(f'quote from 0x.org: {response.json()}')
            return response
        except Exception as e:
            print(response.json())
            raise e 
        
import hmac
import base64
import datetime

from . import consts as c

def sign(message, secretKey):
    mac = hmac.new(bytes(secretKey, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
    d = mac.digest()
    return base64.b64encode(d)


def pre_hash(timestamp, method, request_path, body, debug = True):
    if debug == True:
        print(f'body: {body}')
    return str(timestamp) + str.upper(method) + request_path + body


def get_header(project_id, api_key, sign, timestamp, passphrase, debug = True):
    header = dict()
    header[c.CONTENT_TYPE] = c.APPLICATION_JSON
    header[c.OK_ACCESS_PROJECT] = project_id
    header[c.OK_ACCESS_KEY] = api_key
    header[c.OK_ACCESS_SIGN] = sign
    header[c.OK_ACCESS_TIMESTAMP] = str(timestamp)
    header[c.OK_ACCESS_PASSPHRASE] = passphrase
    if debug == True:
        print(f'header: {header}')
    return header

def parse_params_to_str(params):
    url = '?'
    for key, value in params.items():
        if(value != ''):
            url = url + str(key) + '=' + str(value) + '&'
    url = url[0:-1]
    return url


def get_timestamp():
    now = datetime.datetime.now()
    t = now.isoformat("T", "milliseconds")
    return t + "Z"


def signature(timestamp, method, request_path, body, secret_key):
    if str(body) == '{}' or str(body) == 'None':
        body = ''
    message = str(timestamp) + str.upper(method) + request_path + str(body)

    mac = hmac.new(bytes(secret_key, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
    d = mac.digest()

    return base64.b64encode(d)