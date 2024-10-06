import requests
from bs4 import BeautifulSoup
import re

currencies_dict = {
    "ووچر": "PMUSD-Perfect-Money-USD",
    "تتر": "USDT-Tether",
    "بیت کوین": "BTC-Bitcoin",
    "اتریوم": "ETH-Ethereum",
    "نات کوین": "NOT-Notcoin",
}

def currency_rate(currency):

    name = currencies_dict[currency]

    url = f"https://sarmayex.com/currencies/{name}"

    page = requests.get(url)

    soup = BeautifulSoup(page.text, "html.parser")

    script = soup.find("span", class_ = "text-lg font-bold")

    for detail in script:
        if "," in detail:
            currency_price = int(re.sub(",", "", detail.text.strip()))
            return int(currency_price)
        return float(detail)


  
