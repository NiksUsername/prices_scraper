import time
from datetime import datetime, timedelta

from curl_cffi import requests
from bs4 import BeautifulSoup

from discount_properties import is_big_discount

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.234 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Connection': 'keep-alive',
    'Cookie': 'requestId=f6b74973-d650-41d4-95f2-289422218e5b; form_key=sifpoRU80jL1pWxH; mage-cache-storage={}; mage-cache-storage-section-invalidation={}; mage-cache-sessid=true; _br_uid_2; recently_viewed_product={}; recently_viewed_product_previous={}; recently_compared_product={}; recently_compared_product_previous={}; product_data_storage={}; mage-messages=; bv_metrics=true'
}

cookies = {
    'form_key':	"sifpoRU80jL1pWxH",
    'mage-cache-sessid':	"true",
    'mage-cache-storage':	"{}",
    'mage-cache-storage-section-invalidation':	"{}",
    'mage-messages':	"",
    'product_data_storage':	"{}",
    'recently_compared_product':	"{}",
    'recently_compared_product_previous':	"{}",
    'recently_viewed_product':	"{}",
    'recently_viewed_product_previous':	"{}",
    'requestId':	"f6b74973-d650-41d4-95f2-289422218e5b"
}

prices = {}

temporary_discounts = {}

def get_new_prices(url, page_number=1):
    response = requests.get(url+f"?p={page_number}&product_list_limit=192", headers=header, cookies=cookies, impersonate="chrome120")

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        items = soup.find_all('li', class_='product-item')

        discounts_list = []
        for item in items:
            label = item.find('a', class_='product-item-link')
            name = label.text.strip()
            old_price = item.find('span', class_='price-was_price')
            if old_price:
                old_price = float(old_price.find("span", class_="price").text.strip().replace("£", "").replace(",", ""))
                price = float(item.find('span', class_='price-including-tax').find("span", class_="price").text.strip().replace("£", "").replace(",", ""))
            else:
                price = float(item.find('span', class_='price').text.strip().replace("£", "").replace(",", ""))
                old_price = price
            link = label['href']

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

        item_count = int(soup.find_all("span", class_="toolbar-number")[2].text.strip())
        if 196*page_number < item_count:
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
        return []