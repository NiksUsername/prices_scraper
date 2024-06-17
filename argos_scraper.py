import time
from datetime import datetime, timedelta

from curl_cffi import requests
from bs4 import BeautifulSoup

import keepa_manager
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
    'Cookie': 'analytics_channel=mcomm; _abck=F00624B0353064CB97EE9E72FB0043F3~0~YAAQj6wQAiqKugqQAQAAe5tXJwy/XB8MMYoanU1iMiABVTqVtrKCTsqHTOwS7QpYSkNo+u0jR7vqE4WwvNNyg3y2DSoZL05R1s2ezQZcUiQMcnyabSoy/xoP1GRwnqBBobEKke5RTaMd9YCN5K/Pz7rpnDwCA8la4LYFLJqcXuY9JBW3IFVIXIqRBLBgCUGE7u0wdsac/ZwNmv9+660+EtIPjiorq5Vs21ENZMdFMgUJVA/m4vSBHSuerZdnk/d9yKil+QVx0QEuXG1L5DzZYaJe+RtsnVhdYML6xCCtrxnvjVWwjdkWMIYLDlio+Fo6aeG2Wv7L8wM9KJ414Q47oAm5eW7nx1EtjyrQTfRfq+S0jbUeGP/DyBOoXJOx+6T89eFWCrzFhKg0K52w~-1~-1~-1; utag_main=v_id:018dacfc0c9c004ff495…F56q2cDduH2Xtk7bTyun+UU/FQXRC9MGLswIayzLxQ3vQhR1VytAi81pl1TIWM1gHms/ZQ==~1; bm_ss=ab8e18ef4e; bm_mi=D038DA41A5A2C573EF017490A2132FF4~YAAQj6wQAk6HugqQAQAAOXVXJxjGgIDRFwqpRD78MsDBGA02qumYbtQPLNtsu8ac66QWcj88rB5P8JBYWjVcoJf+mUwlPch/UqtBTImZ5Rw3PrrEvXPbUzTKaZ+jlwsVhBcCR3sH6yGEpSRj/BXC7ji+CO7F8og8NWSDJfaHssT0++XgPJ764f2vfnCkLyuj0d7HCoLlyNX1BV4sZSfhib2eGuH55i54TQfv/2t4Dc/1pFkPjX+a3wJrzp7In7+CdPEZrco0Fp4iCU+aEE0WPVprNoSyxnMCuajYwijEr62YFTEA4O+9a/zV21Ea72c8VKH5YSek/AlBKYXyVt1BvWRL6sFWoJ8pNtCuI+rYDwWba+3nTjo55A==~1'
}

cookies = {
    "_abck": "F00624B0353064CB97EE9E72FB0043F3~0~YAAQj6wQAiqKugqQAQAAe5tXJwy/XB8MMYoanU1iMiABVTqVtrKCTsqHTOwS7QpYSkNo+u0jR7vqE4WwvNNyg3y2DSoZL05R1s2ezQZcUiQMcnyabSoy/xoP1GRwnqBBobEKke5RTaMd9YCN5K/Pz7rpnDwCA8la4LYFLJqcXuY9JBW3IFVIXIqRBLBgCUGE7u0wdsac/ZwNmv9+660+EtIPjiorq5Vs21ENZMdFMgUJVA/m4vSBHSuerZdnk/d9yKil+QVx0QEuXG1L5DzZYaJe+RtsnVhdYML6xCCtrxnvjVWwjdkWMIYLDlio+Fo6aeG2Wv7L8wM9KJ414Q47oAm5eW7nx1EtjyrQTfRfq+S0jbUeGP/DyBOoXJOx+6T89eFWCrzFhKg0K52w~-1~-1~-1",
    "_cls_s": "83163b84-2088-4dce-b68c-dc371616079d:0",
    "_cls_v": "9da0bcf3-1541-4815-b22b-6738aa4b3584",
    "_taggstar_exp": "v:3|id:|group:",
    "_taggstar_vid": "2dca6491-d708-11ee-8214-537a6449f81f",
    "ak_bmsc": "03EA36E8410BE1DD848A2F8AA61D8FCE~000000000000000000000000000000~YAAQj6wQAlKHugqQAQAAVXVXJxhhsiSqgzcrcZkJS7SxtwwgjUEORpIZySrpLq7dW8myhbhOtmL36NO+BkEFacyHAc+kI1PzaYDOWNp/C0Q/Td4Sw2k3GEcDa7kPI80glyVYjmqgTMTzkzbM2UVRY+xFWEktMB0mS5+JtxxoAha1woOXfGR1mPV9rI0hnC/L3jhmlAZBOqOjy5SBHbo51uvU052g9AbS4IIMQREG691nmHpARR0q0a6rXzj5TvQFmGbQOpPYEDYH+vRGzPAwAXeirFZXJgVI7ue2G/88Ppqg2Zp196IoUFYzxCsUdfjbkBdDOTVybMExfsqOmNp6XC+OiBZDFDx1RBJFdEtgvL81MQZ40Lj4RbRi0fEdbDPUyM1De2ZsjKJ6UT0=",
    "akaas_arg_uk_global": "1719856560~rv=12~id=e8706af1c491cc3f9a89c201336bbb88",
    "akaas_arg_uk_pm_dxc": "100",
    "akavpau_vpc_gcd": "1718474904~id=816b362b3a8f3c1f7f55decb76b18ad9",
    "akavpau_vpc_pdpcd": "1718474929~id=6fb5f1209c9970448350ebf2b2ddbcd1",
    "AMCV_095C467352782EB30A490D45@AdobeOrg": "179643557|MCIDTS|19892|MCMID|87286231597634338936380337387751060019|MCAID|NONE|MCOPTOUT-1718654161s|NONE|vVersion|5.5.0",
    "AMCVS_095C467352782EB30A490D45@AdobeOrg": "1",
    "analytics_channel": "mcomm",
    "Apache": "10.102.16.99.1718473615020850",
    "argos_cis_delay_refresh": "true",
    "ArgosPopUp_customer1In20Chance": "false",
    "AWSALB": "+uYI4Xfj/73xCc7NkQUvKlwninbZFQ2mPzQuFD5vMVIhdTUZetrEzU0uGsHKCxuLiyEOQDXoUjeWrt4CVKDIk66gDXYX32RuIlnM90YDWKcNaPWVYQo5YBwoaW8X",
    "AWSALBCORS": "+uYI4Xfj/73xCc7NkQUvKlwninbZFQ2mPzQuFD5vMVIhdTUZetrEzU0uGsHKCxuLiyEOQDXoUjeWrt4CVKDIk66gDXYX32RuIlnM90YDWKcNaPWVYQo5YBwoaW8X",
    "Bc": "d:1*1_p:0*0.005_r:null*null",
    "bm_mi": "D038DA41A5A2C573EF017490A2132FF4~YAAQj6wQAk6HugqQAQAAOXVXJxjGgIDRFwqpRD78MsDBGA02qumYbtQPLNtsu8ac66QWcj88rB5P8JBYWjVcoJf+mUwlPch/UqtBTImZ5Rw3PrrEvXPbUzTKaZ+jlwsVhBcCR3sH6yGEpSRj/BXC7ji+CO7F8og8NWSDJfaHssT0++XgPJ764f2vfnCkLyuj0d7HCoLlyNX1BV4sZSfhib2eGuH55i54TQfv/2t4Dc/1pFkPjX+a3wJrzp7In7+CdPEZrco0Fp4iCU+aEE0WPVprNoSyxnMCuajYwijEr62YFTEA4O+9a/zV21Ea72c8VKH5YSek/AlBKYXyVt1BvWRL6sFWoJ8pNtCuI+rYDwWba+3nTjo55A==~1",
    "bm_s": "YAAQj6wQAjmHugqQAQAAsnRXJwHMGlVAKwOiX3S/4R7vK7zPZtM1lVsiZfMO9wBmXBuyiP2Kh+g2AM5tDyf4czmWF3Ygdh7y62OmwKFWaF19nE7oymCoHqrwQYu2VZXiyw7aVy0QpQWE5sEAfOdnE9LY2H07h+OY6Ct7yUYVl1voESCxctEfTx4jH7RjZ08la7JugJV7IzQOBWQgLe0XMVQvuk/IzbP/Ai1JB6fVRBiyU0C5lzygzSqQ5Q9SXdflIr5NgbgmZBwlE3FJDeitIAAbCjEY11dnAARulgWfWCMY+baI17RNWgzd0VmwR36OI4CIZvN6DbPMXR+deInT4wbnGCQZaEWC",
    "bm_ss": "ab8e18ef4e",
    "bm_sv": "74985B8B6605D0C8065002B67A06C618~YAAQj6wQAueJugqQAQAARpdXJxixiygcC2E4p14Uf7WEN5sBzbaiHsAtR5GT6rqpfpNBeZlOwftt4cElzPIhmASofk+KCRRHD7nCEPfEBEdTVd9ZolmFS2jKrFyi4eQ1HfPOu6gNZMTl/dQOnrcZhnIPPiiwnKp7/jX32zWlt3kyOWiTaTiICR4NKMG1F56q2cDduH2Xtk7bTyun+UU/FQXRC9MGLswIayzLxQ3vQhR1VytAi81pl1TIWM1gHms/ZQ==~1",
    "bm_sz": "39C2FB8FDD67CF57D3CCD3B3AB690C48~YAAQj6wQApyEugqQAQAAglxXJxh1pDqOXZtQnymN8AKdJ+x9vc6Hso/uuvYv6CSR4rZ7wMIKCHsgUCK+gsriItMezQVZKGB380RpbKVtS1CMObcL859BRt2xzdByVTi101ylRC43Ku+9D3lN9mAzYLNhmYxt1fHXoaDaJFIQED68Pkhybu3i8eQUYyYhSkxCQTxJF/eboDBLPiamjsiO7ea46MHk8hFepyjgl0xqxopHSGwW7kYMMFOWX6q8AR9HFSy/oI54rP+gscX8hajfbWbM70mqWzL5fXYkRKdz+n6mLmd4mHp8kiw3UZRuIF47iH5lkmR4/NXgfIFJtWoN8d3j34SyT60SjJWFKI0JSKozl7A3iSuhjA==~3290180~3356993",
    "Checkout_Test_Group_2": "NEW_HD|NEW_HD_SI|NEW_HD_LI",
    "cisId": "8f5ec92af9ae4acfba8952736509d390",
    "CONSENTMGR": "consent:true|ts:1718444037019|id:018dacfc0c9c004ff4950a12766c05050005700d00bd0",
    "Content_Test_Group_1": "2",
    "JSESSIONID": "0000kqCCqGU95DQQqPLWayqhJoH:1fa25sk9e",
    "localisationTooltip": "open",
    "mdr_browser": "Akamai",
    "PDP_Test_Group_1": "2",
    "PostCodeSessionCookie": ",M11AA,",
    "prev_vals": "ar:pdp:1180778:amazonkindlepaperwhitesignatureed32gbwi-fie-reader:*|*ar:productdetails:",
    "pwd_email": "new",
    "sessionId": "I3D82BBqnKS767BeIxicKX7TsVC0ChWsH5DyemS/TVOpxxZQzQdkHohf+9nW1V+/",
    "sids": "WyI2NjEiXQ==",
    "syte_ab_tests": "{}",
    "syte_uuid": "20b4f410-fd8d-11ee-829e-9557f3b9dbbe",
    "ufvd": "~abTestVariantGroup-B~clp_29203-U!brands_tommy-hilfiger-U!clp_29949-e!brands_amazon-e",
    "umdid": "NDZmZDA1NTEtZjViYS00ZDlhLTkwYzEtMGEwZTY4N2I1M2YwfGNhM2M1NTJkLWU4MjUtNDE2OS05YTliLTRjZDY3ZWJiZDBjOHww",
    "UserPersistentSessionCookie": "13907625476;;UNKNOWN;;GIFT_NO;10.102.16.99.1718473615020850;REMEMBER_NO;;false;",
    "UserRegistrationType": "R",
    "utag_main": "v_id:018dacfc0c9c004ff4950a12766c05050005700d00bd0$_sn:14$_se:5$_ss:0$_st:1718648761717$vapi_domain:argos.co.uk$dc_visit:14$ses_id:1718646956285;exp-session$_pn:1;exp-session$dc_event:3;exp-session",
    "WC_ACTIVEPOINTER": "110,10151",
    "WC_AUTHENTICATION_-1002": "-1002,5Ce8ewpCVheUcD8tRlGdytomv7Q=",
    "WC_GENERIC_ACTIVITYDATA": "[108868518808:true:false:0:hUrseY/scy1bn+t4IPc9kUxc0OM=][com.ibm.commerce.context.audit.AuditContext|1718473615021-776277][com.ibm.commerce.store.facade.server.context.StoreGeoCodeContext|null&null&null&null&null&null][CTXSETNAME|Store][com.ibm.commerce.context.globalization.GlobalizationContext|110&GBP&110&GBP][com.ibm.commerce.catalog.businesscontext.CatalogContext|10001&null&false&false&false][com.ibm.commerce.context.base.BaseContext|10151&-1002&-1002&-1][com.ibm.commerce.context.experiment.ExperimentContext|null][com.ibm.commerce.context.entitlement.EntitlementContext|4000000000000000002&4000000000000000002&null&-2000&null&null&null][com.ibm.commerce.giftcenter.context.GiftCenterContext|null&null&null]",
    "WC_PERSISTENT": "pa03nxNWKE7QlSmysYEeY7wpVcA=\n;2024-06-17+18:56:01.231_1718473615021-776277_10151_-1002,110,GBP_10151",
    "WC_SESSION_ESTABLISHED": "true",
    "WC_USERACTIVITY_-1002": "-1002,10151,0,null,-1,null,13907625476,/webapp/wcs/stores/servlet/GetUserInfo?catalogId=10001&langId=110&storeId=10151,null,null,W+64k5Zha/3TeJbmNk2RYEhWckxYejV9jm7TuU9UFYU0QCdJFTy3jPx6FPVEwSA+HPHbZwb/hv/L4cp9bB5Hx2l4YKCiS9vym+qQMZnfNbUFnswxQe1S8dNUg0Eqjmno8fVeVxJpGSchhyGW0jcPt8fRJUMcNgRuPEpPq1MoJSDkL/aDL/pMby2QSR2ONNAMXH7zKhjDFo034hZrocq8jCaRnAoL+LHcjbJjU5iv2nHuBw0EA3o0KixidQQJyzZHqlEbABSJOFTnuJQ6CnmjxpGnUn42A6NxT5/m5jR03kPVxTj/6DS8LPAWLZrKn7tC"
}

prices = {}

temporary_discounts = {}


def get_new_prices(url, page_number=1):
    response = requests.get(url+f"opt/page:{page_number}/", headers=header)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        items = soup.find_all('div', class_='ProductCardstyles__ContentBlock-h52kot-5')

        discounts_list = []
        for item in items:
            name = item.find('div', class_='ProductCardstyles__Title-h52kot-12').text.strip()
            price = float(item.find('div', class_='ProductCardstyles__PriceText-h52kot-16').text.strip().replace("£", ""))
            old_price = item.find("div", class_="ProductCardstyles__WasText-h52kot-20")
            if old_price:
                old_price = float(old_price.text.replace("Was", "").strip().replace("£", ""))
            else:
                old_price = price
            link = "https://www.argos.co.uk" + item.find('a', class_='ProductCardstyles__Link-h52kot-13')['href'].split("?")[0]
            image = f"https://media.4rgos.it/s/Argos/{link.split('/')[4].split('?')[0]}_R_SET?w=270&h=270&qlt=75&fmt.jpeg.interlaced=true"

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

        item_count = int(soup.find("span", class_="styles__ResultsCount-sc-1hkcas-11")["data-search-results"])
        if 60*page_number < item_count:
            time.sleep(1)
            for discount in get_new_prices(url,page_number+1):
                discounts_list.append(discount)

        temp = temporary_discounts.items()
        for key, value in temp:
            if value < datetime.now() - timedelta(hours=12):
                temporary_discounts.pop(key)
        return discounts_list

    else:
        print("Failed to retrieve argos page")
        return []


def get_keepa_results(price_drops):
    keepa_drops = []
    for price_drop in price_drops:
        if price_drop["old_price"] == 0 or price_drop["price"]/price_drop["previous_price"] <= 0.85:
            bar_code = get_bar_code(price_drop["link"])
            if not bar_code:
                compare_price, fee, fee_percentage, asin, avg90 = keepa_manager.get_from_title(price_drop["name"])
            else:
                compare_price, fee, fee_percentage,asin,avg90 = keepa_manager.get_from_bar_code(bar_code)

            if not compare_price:
                continue
            profit = compare_price-price_drop["price"]-0.5-(compare_price/6 - price_drop["price"]/6) - fee - (compare_price*fee_percentage)
            profit_margin = profit/compare_price
            if profit_margin >= 0.15:
                margin_ping = {
                    "keepa_price": compare_price,
                    "price": price_drop["price"],
                    "name": price_drop["name"],
                    "link": price_drop["link"],
                    "margin": profit_margin,
                    "ASIN":asin,
                    "avg": avg90,
                    "image": price_drop["image"]
                }
                keepa_drops.append(margin_ping)
    return keepa_drops


def get_bar_code(link):
    response = requests.get(link, headers=header, cookies=cookies, impersonate="chrome120")
    soup = BeautifulSoup(response.content, 'html.parser')
    description = soup.find("div", class_="product-description-content-text")
    lines = description.find_all("li")
    if len(lines) > 0 and "EAN:" in lines[len(lines)-1].text:
        return lines[len(lines)-1].text.replace("EAN:", "").replace(".", "").strip()
    return None

