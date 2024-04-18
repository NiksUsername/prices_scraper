import math

import requests

import config


def get_from_bar_code(bar_code):
    url = f"https://api.keepa.com/product?key={config.KEEPA_API}&domain=2&code={bar_code}&stats=7"
    content = requests.get(url).json()
    try:
        content["products"][0]
    except:
        return None, None, None, None, None
    try:
        price = content["products"][0]["stats"]["current"][1]/100
        avg90 = content["products"][0]["stats"]["avg90"][1]/100
        if price<0:
            raise Exception
        if avg90<0:
            avg90="N/A"
        else:
            avg90=f"£{round(avg90, 2)}"
        fba_fee = content["products"][0]["fbaFees"]
        fba_fee = fba_fee["pickAndPackFee"] if fba_fee else 0
        fba_fee = fba_fee/100 if fba_fee and fba_fee > 0 else 0
        percentage_fee = content["products"][0].get("referralFeePercentage")
        percentage_fee = percentage_fee/100 if percentage_fee else 0
        asin = content["products"][0]["asin"]

        return price, fba_fee, percentage_fee, asin, avg90
    except Exception:
        return None, None, None, None, None

get_from_bar_code("043859726738")