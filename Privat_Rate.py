import requests
from datetime import datetime

now = datetime.now()
current_date = now.strftime("%d.%m.%Y")

response = requests.get(f'https://api.privatbank.ua/p24api/exchange_rates?json&date={current_date}')
def find_rate(currency):
    for item in response.json()["exchangeRate"]:
        if item["currency"] == currency:
            return item
    return None

usd_rate = find_rate("USD")
eur_rate = find_rate("EUR")
gel_rate = find_rate("GEL")
pln_rate = find_rate("PLN")
huf_rate = find_rate("HUF")

rate_privat_to_uah = str(current_date)
rate_privat_to_uah += f'\n\nUSD: {usd_rate.get("purchaseRate")}' \
                      f'/ {usd_rate.get("saleRate")}'
rate_privat_to_uah += f'\n\nEUR: {eur_rate.get("purchaseRate", "N/A")}' \
                      f'/ {eur_rate.get("saleRate")}'
rate_privat_to_uah += f'\n\nGEL: {gel_rate.get("purchaseRateNB")}' \
                      f'/ {gel_rate.get("saleRateNB", "N/A")}'
rate_privat_to_uah += f'\n\nPLN: {pln_rate.get("purchaseRate")}' \
                      f'/ {pln_rate.get("saleRate")}'
rate_privat_to_uah += f'\n\nHUF: {huf_rate.get("purchaseRateNB")}' \
                      f'/ {huf_rate.get("saleRateNB")}'

privat_uah_to_all = {
    'USD': float(usd_rate.get("saleRate")),
    'EUR': float(eur_rate.get("saleRate")),
    'GEL': float(gel_rate.get("saleRateNB")),
    'PLN': float(pln_rate.get("saleRate")),
    'HUF': float(huf_rate.get("saleRateNB"))
}