import time
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

import links
from discount_properties import is_big_discount

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Connection': 'keep-alive'
}

prices = {}
temporary_discounts = {}


def get_new_prices(url, page_number=1, chunk=1):
    url_id = url.replace("https://www.johnlewis.com/browse/", "").replace("/", ",").replace(",_,", ",show-in-stock-items-only,_,")
    api_url = f"https://www.johnlewis.com/standard-plp/api/product-chunks?page={page_number}&chunk={chunk}&term=&type=browse&facetId={url_id}&sortBy=&price=&priceBands=&listHead=&lolcode="
    response = requests.get(api_url, headers=header)
    discounts_list = []

    if response.status_code == 200:

        items = response.json()

        for item in items:
            name = item["title"]
            try:
                price = float(item["price"]["now"].replace(",", ""))
            except:
                price = float(item["price"]["now"]["from"].replace(",", ""))

            if item["price"]["was"]:
                try:
                    old_price = float(item["price"]["was"].replace(",", ""))
                except:
                    old_price = float(item["price"]["was"]["from"].replace(",", ""))
            else:
                old_price = price
            link = "https://www.johnlewis.com/item/p"+str(item["id"])

            item_data = {
                "name": name,
                "price": price,
                "link": link,
                "old_price": old_price
            }
            if link in prices:
                if prices[link]["old_price"] != price and price != prices[link]["price"] and link not in temporary_discounts and is_big_discount(item_data):
                    item_data["old_price"] = prices[link]["old_price"]
                    prices[link]["price"] = price
                    discounts_list.append(item_data)
                    temporary_discounts[link] = datetime.now()
                elif link not in temporary_discounts:
                    if prices[link]["old_price"] < old_price:
                        prices[link]["old_price"] = old_price
                    prices[link]["price"] = price
            else:
                prices[link] = item_data.copy()
                #item_data["old_price"] = 0
                #discounts_list.append(item_data)

        if len(items) >= 24:
            time.sleep(0.5)
            if chunk == 8:
                page_number += 1
                chunk = 1
            else: chunk += 1
            for discount in get_new_prices(url, page_number, chunk):
                discounts_list.append(discount)

        temp = temporary_discounts.items()
        for key, value in temp:
            if value < datetime.now() - timedelta(hours=24):
                temporary_discounts.pop(key)
        return discounts_list

    else:
        print("Failed to retrieve the page")
        return discounts_list