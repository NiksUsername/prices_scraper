import time
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

import keepa_manager
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


def get_new_prices(url, page_number=1):

    response = requests.get(url+f"?pageNumber={page_number}&productsOnly=True", headers=header)
    discounts_list = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        items = soup.find_all('div', class_='OfferBox')

        for item in items:
            name = item.find('a', class_='offerboxtitle')
            price = float(item.find('span', class_='offerprice').text.strip().replace("£", ""))
            old_price = item.find("div", class_="SavingsPrice")
            if old_price:
                old_price = price + float(old_price.text.split("£")[1].strip())
            else:
                old_price = price
            link = "https://www.laptopsdirect.co.uk" + name['href']
            name = name.text.strip()
            image = item.find("img", class_="offerImage")["src"]

            item_data = {
                "name": name,
                "price": price,
                "link": link,
                "old_price": old_price,
                "image": image
            }
            if link in prices:
                item_data["old_price"] = prices[link]["old_price"]
                if prices[link]["old_price"] > price and price != prices[link]["price"] and link not in temporary_discounts:
                    item_data["old_price"] = prices[link]["old_price"]
                    item_data["previous_price"] = prices[link]["price"]
                    prices[link]["price"] = price
                    discounts_list.append(item_data)
                    temporary_discounts[link] = datetime.now()
                elif link not in temporary_discounts:
                    if prices[link]["old_price"] < old_price:
                        prices[link]["old_price"] = old_price
                    prices[link]["price"] = price
            else:
                prices[link] = item_data.copy()
                item_data["old_price"] = 0
                discounts_list.append(item_data)

        all_items = soup.find_all("div", "OfferBoxPrice")
        if len(all_items) >= 48:
            time.sleep(0.5)
            for discount in get_new_prices(url,page_number+1):
                discounts_list.append(discount)

        temp = temporary_discounts.items()
        for key, value in temp:
            if value < datetime.now() - timedelta(hours=24):
                temporary_discounts.pop(key)
        return discounts_list

    else:
        print("Failed to retrieve the page")
        return discounts_list


def get_keepa_results(price_drops):
    keepa_drops = []
    for price_drop in price_drops:
        if price_drop["old_price"] == 0 or price_drop["price"]/price_drop["previous_price"] <= 0.85:

            compare_price, fee, fee_percentage, asin, avg90 = keepa_manager.get_from_title(price_drop["name"])
            if not compare_price:
                continue
            profit = compare_price - price_drop["price"] - 0.5 - (compare_price / 6 - price_drop["price"] / 6) - fee - (
                        compare_price * fee_percentage)
            profit_margin = profit / compare_price
            if profit_margin >= 0.15:
                margin_ping = {
                    "keepa_price": compare_price,
                    "price": price_drop["price"],
                    "name": price_drop["name"],
                    "link": price_drop["link"],
                    "margin": profit_margin,
                    "ASIN": asin,
                    "avg": avg90,
                    "image": price_drop["image"]
                }
                keepa_drops.append(margin_ping)
    return keepa_drops