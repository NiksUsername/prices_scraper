import time
from datetime import datetime, timedelta

from curl_cffi import requests
from bs4 import BeautifulSoup

from discount_properties import is_big_discount
header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.234 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Connection': 'keep-alive',
    "X-Requested-With": "XMLHttpRequest",
    "Api-Key": "sh5d2d2ph9rgbps3ntrshxqn",
    "Cookie": 'utag_main=v_id:018d994d1bcf001cd2c3728cdee805050005200d00bd0$_sn:5$_ss:1$_st:1711738582010$dc_visit:5$_pn:1%3Bexp-session$ses_id:1711736759098%3Bexp-session$dc_event:1%3Bexp-session; cf_clearance=R6m3nSnPa0u5Q3cWFxr2xwbiK7.yWM9506oTUCRsIZA-1711717168-1.0.1.1-lvgAbJDcKdT.lpTo8kZjYZ9TfVRzldH5ULM5uLNk65_Da537trH_hjqVA1vekwYDq91AfVhYcGHKnVimim31HQ; utag_chan={"channel":"","channel_set":"","channel_converted":false,"awc":""}; CONSENTMGR=consent:true%7Cts:1711706920402; COOKIE_NOTICE_SEEN=seen; SIGNUP_POPUP_SEEN=seen; NEWSLETTER_DISMISSED=true; _cfuvid=fKg1EVNWZYY6YE.4.wKLjgz5J6SmVGfk0NtJAp_wZT0-1711706888561-0.0.1.1-604800000; SF_COUNTRY_LANG=GB_en; JSESSIONID=00009mDNHdTGf9_2wbHkBZeyVvp:-1; __cf_bm=LQdwcCFCoFskM3VF4BTTp3.2yWIVQQug8fT_puITOLc-1711736734-1.0.1.1-.WFL_EFbdlyQ81cWAhWjOLIZxogv60vUqYBybjsEmyR6NGtcsd.B8oXZPttOXRyJWmbLe28tUlZpDtvqJsloE7egkRzxXV85wACDC2fOxWI; _cs_mk=0.3106511578746557_1711736763450'
}

cookies = {
    '__cf_bm':	"LQdwcCFCoFskM3VF4BTTp3.2yWIVQQug8fT_puITOLc-1711736734-1.0.1.1-.WFL_EFbdlyQ81cWAhWjOLIZxogv60vUqYBybjsEmyR6NGtcsd.B8oXZPttOXRyJWmbLe28tUlZpDtvqJsloE7egkRzxXV85wACDC2fOxWI",
    '_cfuvid':	"fKg1EVNWZYY6YE.4.wKLjgz5J6SmVGfk0NtJAp_wZT0-1711706888561-0.0.1.1-604800000",
    '_cs_mk':	"0.3106511578746557_1711736763450",
    'cf_clearance':	"R6m3nSnPa0u5Q3cWFxr2xwbiK7.yWM9506oTUCRsIZA-1711717168-1.0.1.1-lvgAbJDcKdT.lpTo8kZjYZ9TfVRzldH5ULM5uLNk65_Da537trH_hjqVA1vekwYDq91AfVhYcGHKnVimim31HQ",
    'CONSENTMGR':	"consent:true|ts:1711706920402",
    'COOKIE_NOTICE_SEEN':	"seen",
    'JSESSIONID':	"00009mDNHdTGf9_2wbHkBZeyVvp:-1",
    'NEWSLETTER_DISMISSED':	"true",
    'SF_COUNTRY_LANG':	"GB_en",
    'SIGNUP_POPUP_SEEN':	"seen",
    'utag_chan':	'{"channel":"","channel_set":"","channel_converted":false,"awc":""}',
    'utag_main':	"v_id:018d994d1bcf001cd2c3728cdee805050005200d00bd0$_sn:5$_ss:1$_st:1711738582010$dc_visit:5$_pn:1;exp-session$ses_id:1711736759098;exp-session$dc_event:1;exp-session"
}

prices = {}
temporary_discounts = {}


def get_new_prices(url, page_number=1):
    link = f"{url}&page={page_number}&productsPerPage=400&sortOption=rank&selectedFilters=&isSearch=false&searchText=&columns=4&mobileColumns=2&clearFilters=false&pathName=/gaming/xbox&searchTermCategory=&selectedCurrency=GBP&portalSiteId=318&searchCategory="
    response = requests.get(link, headers=header, cookies=cookies, impersonate="chrome120")
    discounts_list = []

    if response.status_code == 200:
        items = response.json()

        discounts_list = []
        for item in items["products"]:
            name = f'{item["name"]} - {item["brand"]}'
            price = float(item["price"].replace("£", "").replace(",", ""))
            old_price = item["ticketPrice"]
            if old_price:
                old_price = float(old_price.replace("£", "").replace(",", ""))
            else:
                old_price = price
            link = "https://www.houseoffraser.co.uk/" + item["url"]

            item_data = {
                "name": name,
                "price": price,
                "link": link,
                "old_price": old_price
            }
            if link in prices:
                if prices[link]["old_price"] > price and price != prices[link]["price"] and link not in temporary_discounts:
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
                # item_data["old_price"] = 0
                # discounts_list.append(item_data)

        item_count = int(items["numberOfProducts"])
        if 400 * page_number < item_count:
            time.sleep(0.5)
            for discount in get_new_prices(url, page_number + 1):
                discounts_list.append(discount)

        temp = temporary_discounts.items()
        for key, value in temp:
            if value < datetime.now() - timedelta(hours=12):
                temporary_discounts.pop(key)
        return discounts_list

    else:
        print("Failed to retrieve house of fraser page")
        return discounts_list