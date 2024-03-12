import time
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

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
            link = "https://www.laptopsdirect.co.uk" + name['href']
            name = name.text.strip()

            item_data = {
                "name": name,
                "price": price,
                "link": link
            }
            if link in prices:
                if prices[link]["price"]*0.99 >= price:
                    item_data["old_price"] = prices[link]["price"]
                    prices[link]["price"] = price
                    discounts_list.append(item_data)
                    temporary_discounts[link] = datetime.now()
                elif link not in temporary_discounts:
                    prices[link] = item_data.copy()
            else:
                prices[link] = item_data.copy()
                #item_data["old_price"] = 0
                #discounts_list.append(item_data)

        all_items = soup.find_all("div", "OfferBoxPrice")
        if len(all_items) >= 48:
            time.sleep(1)
            for discount in get_new_prices(url,page_number+1):
                discounts_list.append(discount)

        temp = temporary_discounts.items()
        for key, value in temp:
            if value < datetime.now() - timedelta(hours=12):
                temporary_discounts.pop(key)
        return discounts_list

    else:
        print("Failed to retrieve the page")
        return discounts_list

