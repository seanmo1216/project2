import os

from binance.client import Client

api = os.environ.get('binance_api')
secret = os.environ.get('binance_secret')

client = Client(api, secret)

