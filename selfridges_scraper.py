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
    category = url.split("/cat/")[1].replace("/", "|")
    category = category[0:len(category)-1]
    api_url = f"https://www.selfridges.com/api/cms/ecom/v1/GB/en/productview/byCategory/byIds?ids={category}&pageNumber={page_number}&pageSize=180"
    print(api_url)
    #api_url = "https://www.selfridges.com/api/cms/ecom/v1/GB/en/productview/byCategory/byIds?ids=home-tech%7Ctechnology&pageNumber=1&pageSize=100"
    response = requests.get(api_url, headers=header, cookies=cookies, impersonate="chrome120")
    print(response.content)
    print(response.text)
    print(response.json())
    discounts_list = []

    if response.status_code == 200:

        items = response.json()

        for item in items["catalogEntryNavView"]:
            name = item["name"]
            price_object = item["price"][0]
            price = float(price_object["lowestPrice"])
            old_price = price_object.get("lowestWasWasPrice")
            if old_price:
                old_price = float(old_price)
            else:
                old_price = price_object.get("lowestWasPrice")
                if old_price:
                    old_price = float(old_price)
                else:
                    old_price = price
            link = "https://www.selfridges.com/GB/en/product/"+str(item["seoKey"])

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

        item_count = int(items["recordSetTotal"])
        if 180 * page_number < item_count:
            time.sleep(1)
            for discount in get_new_prices(url, page_number + 1):
                discounts_list.append(discount)

        temp = temporary_discounts.items()
        for key, value in temp:
            if value < datetime.now() - timedelta(hours=24):
                temporary_discounts.pop(key)
        return discounts_list

    else:
        print("Failed to retrieve the page")
        return discounts_list
