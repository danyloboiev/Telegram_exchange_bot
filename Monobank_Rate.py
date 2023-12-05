import requests
from datetime import datetime

now = datetime.now()
current_date = now.strftime("%d.%m.%Y")

response = requests.get('https://api.monobank.ua/bank/currency')
rate_monobank_to_uah = f'{current_date}'
rate_monobank_to_uah += f'\n\nUSD: {response.json()[0]["rateBuy"]} / {response.json()[0]["rateSell"]}'
rate_monobank_to_uah += f'\n\nEUR: {response.json()[1]["rateBuy"]} / {response.json()[1]["rateSell"]}'
rate_monobank_to_uah += f'\n\nGEL: {response.json()[36]["rateCross"]}'
rate_monobank_to_uah += f'\n\nPLN: {response.json()[79]["rateCross"]}'
rate_monobank_to_uah += f'\n\nHUF: {response.json()[42]["rateCross"]}'

mono_uah_to_all = {
    'USD': float(response.json()[0]["rateSell"]),
    'EUR': float(response.json()[1]["rateSell"]),
    'GEL': float(response.json()[36]["rateCross"]),
    'PLN': float(response.json()[79]["rateCross"]),
    'HUF': float(response.json()[42]["rateCross"])
}

crnc_type = f'\n\nЗараз ти можеш конвертувати у такі валюти:' \
            f'\nUSD - Долар США' \
            f'\nEUR - Євро' \
            f'\nGEL - Грузинська Ларі' \
            f'\nPLN - Польска злота' \
            f'\nHUF - Угорський Форінт'