from pycoingecko import CoinGeckoAPI
import os
import requests
from kucoin.client import Client

ku_key = os.environ['ku_key']
ku_secret = os.environ['ku_secret']
ku_pass = os.environ['ku_pass']
#
cg = CoinGeckoAPI()
client = Client(ku_key, ku_secret, ku_pass)


# drop kucoin currencies into file
# file = './static/kucoin_cryptos.json'
# with open(file, 'w+') as f:
# 	json.dump(client.get_symbols(), f, indent=2)

# get info about coin
# print(client.get_ticker('OMG-BTC')['price'])


def get_price(ticker):
	price = float(client.get_ticker(ticker)['price'])
	f_price = f"{price:.12f}"
	return f_price


# Kucoin api
# path = '/api/v1/market/histories'
# r = requests.get(ku_base_url+path, params={'symbole':'BTC-USDT'})
# print(r.json())


# Alpaca api get news
def get_news():
	url = f"https://data.alpaca.markets/v1beta1/news?limit=50"
	headers = {
		'Apca-Api-Key-Id': os.environ['Apca-Api-Key-Id'],
		'Apca-Api-Secret-Key': os.environ['Apca-Api-Secret-Key'],
	}

	news = requests.get(url, headers=headers).json()['news']
	return news


def get_trending():
	trending_dict = {}
	trending = cg.get_search_trending()
	for coin in trending['coins']:
		trending_dict[coin['item']['id']] = coin['item']['symbol']
	return trending_dict
