import time
from datetime import datetime, timedelta

from curl_cffi import requests
from bs4 import BeautifulSoup

import keepa_manager
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
    'Connection': 'keep-alive',
    'Cookie': 'analytics_channel=ecomm; _abck=F00624B0353064CB97EE9E72FB0043F3~0~YAAQvHnKF1/mD9SNAQAAA/qdFAvMk9mVVtZhrpBX9rQ25AruU4RPGK8/ixu0ur26qz+2UFQYSazKRnLy7wlhkfg9TuJiUS0MU3Zm5dGZf+1dM1cBmbcHnfuyAnHwPql7o+7PHOPIjJTewG/0vv3b++PXKB2H0Ju5i/J6nq4dXyFtiFrPOnzkGvJOpxOq6lgtRSy60DihntJ2Y7x2R8xhasNs80XweOq6LqmQf/1p8HNimhtayaStLhReJuivc92wbTk/KCYOUf3bn4IsJHZSJjH6fiZwpCLvff+iYIEzna5/8JW4gWgcZ5eKg1RShQrsM/QhdEqv4+t9auJt9CbfG7dD8h8Lg0NS9Edq1n2DXypB0Yt2wzlliT4E7APo0UD/AyQ4tAZyJBkZP3CxKLflFOpSAuO9irMx3Ms=~-1~-1~-1; utag_main=v_id:018dacfc0c9c004ff4950a12766c05050005700d00bd0$_sn:3$_se:49$_ss:0$_st:1709745846025$vapi_domain:argos.co.uk$dc_visit:3$ses_id:1709742556035%3Bexp-session$_pn:17%3Bexp-session$dc_event:46%3Bexp-session; sessionId=I3D82BBqnKS767BeIxicKX7TsVC0ChWsH5DyemS/TVOpxxZQzQdkHohf+9nW1V+/; cisId=df3edbe5444348fb94aada50caa99e64; CONSENTMGR=consent:true%7Cts:1708004268257%7Cid:018dacfc0c9c004ff4950a12766c05050005700d00bd0; AMCV_095C467352782EB30A490D45%40AdobeOrg=179643557%7CMCIDTS%7C19789%7CMCMID%7C87286231597634338936380337387751060019%7CMCAID%7CNONE%7CMCOPTOUT-1709751244s%7CNONE%7CvVersion%7C5.5.0; _cls_v=9da0bcf3-1541-4815-b22b-6738aa4b3584; akaas_arg_uk_global=1710953642~rv=69~id=031734d66bbfafffb2ffaaa01a3e2b87; localisationTooltip=closed; Checkout_Test_Group_2=NEW_HD|NEW_HD_SI|NEW_HD_LI; _taggstar_vid=2dca6491-d708-11ee-8214-537a6449f81f; _taggstar_exp=v:3|id:|group:; prev_vals=ar%3Acat%3Atechnology%3Avideogamesandconsoles%3Aps5%3Aps5games%3A*%7C*ar%3Acat%3A; AMCVS_095C467352782EB30A490D45%40AdobeOrg=1; ArgosPopUp_customer1In20Chance=false; _cls_s=83163b84-2088-4dce-b68c-dc371616079d:0; Bc=d:1*1_p:0*0.005_r:null*null; ufvd=~~clp_29351-e!events_easter-gifts-U!clp_29203-U!clp_29949-Ba; mdr_browser=Akamai; bm_sz=5DD834F92FFA2768F0196948A6815AC8~YAAQrHnKF193uNSNAQAAc/2YFBcyH2PqZrOOciCNQidawAD3EOP/u7y1XesyAvf6NbaSRqOlTBafaSgj7dbq8s+lNe5nF2VF4ybZCeDigfgtjtkZp0YDBxKeA1OF4bkCEiIcHV5yMt22fR4u4opsb50p5xf0kVoXrBA+TDJG7/l5FTJRbFlJBkWAuKpAYHaFZCkZ4LQijU2TRF0oJ+I15hLVaBkh7JPWjbH4+wmrdi9WmqHmOBWmfP1HlnT/JPKqATi15+DwwNQe3bArfD1zxuknGNmthrxR7IUmJQtbahwNUTEaNAXcEXKKNU7creeGKWONWEu5Gbs8sThnPkZOGnpFYTyt4OPlb1offL3kAgjZ9YZdi3ciuA==~4468792~3485749; ak_bmsc=4215E1B6C593A8688598DD9627FD0654~000000000000000000000000000000~YAAQvHnKF+DlD9SNAQAA6tudFBeukAmsssMf8XbnPWJIbEYTPMuBIyMwZ1KdrO0n/O8oepqNuNJjzXEeZJx6t9aJs2WtChbf7Anu5E4h2/+NFvaqHnXQZ9MLxVKpuiZkLzSsWRaCd5IWkhHzjaxcCWWvHB6bK71BOClRecpLcmzB7u9GafzOJxIr2h58Erz3yXa65oTA9EmdqWjSuFGeKdrl583EhcvQGwhwzHHhcHVeOzgre9C9HXTYU5kTsRXTkx0WBmHrOw9QVd1tfBcUr59zaPGwrtLxEozn+NSw4PKRN2wrvmGDfYYkQoR+afXI33Wz7XFdB6RQl42Al8/W6S4O6upuLaDLayfZwHs2rq6rgUxqsvb+utl3MrVd2LZMNC0e+n8XJpdiGRK+AEyYiPRQC5xwIICF6FRLfoG4KPdaGN7blIX/Ghz/MbXX6hO10RnAt63mbMdW5zmZpEWPUHZZAByEJRuC/CGME/NDjb8zIvSAVWZw4a2yo45jtFs613Ot19Vg4Ae9yveYHm4=; bm_sv=489F557737FDBDB0FEB7A4F125462FAF~YAAQrHnKF3yWudSNAQAAHrWvFBdzFfMFUjWKDhOQFEnQ2J6Bk06bVHeFQ6+OUme1DA4nvtez8b95GIfEnIgPhNCWk5NqBPnp9tkO+LWSE/flIAD06q+RUDTpLDaqbeF7Vs7SJn9Ah/+RnRzZEODv1vDJAd7DbXceMMdiDmagRsd0VSgJvf+cTF2ZxjiL80tTzEy/KPOzU38++NCNLH2E5eFfoA2nq6bPVIR8jtvIWfegX5GEsAt/FZTIDKmZKjb9uZc=~1; bm_mi=6EAF1C8E2815941D8F5B4C0524966061~YAAQvHnKFyvjD9SNAQAADmqdFBeaR4nFjLYC9QsjVO8blgedBsFSqWavvpZ+swf/WLshj/hKIcZsmGSB8k4gXR0/l1gdrBPHFaT0Xkh9NYNvmoHSoXDjUZpEDly3bipSx4jKi9CJR/Jz3+6mUTRFAptaxXUsNfRAKFgtV4etLRM09tTe6ZcNQk55o7FX0MfWH1nIsjbxjEg1P5BywfLxkVHe3iTq81jiPljVlMqUbzFYC0oDlLPFWi1wBUSaaxyP3qxxx6xq9hYz3Ixn5KR+RWDs5rvZmXn2WICNE9g7MEjI9cIwY0Bo8NcN1VcoNxe6zi2ilHgYso2bQI+9neLMqnSjKbWnY+UI6O36GYh292+Rc79EigK3JoKVZGwwOkvh4AumjP9ZulEDnWymIpv3zt/OtNoymA==~1; akavpau_vpc_gcd=1709744329~id=61190d81c53eb6701ea7850ecac2d81c'
}

cookies = {
    "_abck":	"F00624B0353064CB97EE9E72FB0043F3~0~YAAQj3nKF0BefOWOAQAAmo6J8Qu3jpU1E2QSc4Ce8/3qyo+gLhzdDg7cHiXrele2uXAI2MvqBNQw/Du4DklY2tw9AsLm7ciYFT/Oi9/fsjCFrsf2UlOs7SH5dmSluVefkK0jsJFENVMrtxTh31ac2epOCFDgYvB4KANwBDEBRirWtXabigpv7zKvyPpERCm1pToVQmRwytzxxaSlmG/pCkXXWAmpVI7fc7hRpVQP1zIyKMiyz9Mnxpp6dzzP6NEFA3XGM4Ypiin5IJnW8OoWYGbeS4HTWTljMNL1Tkbi3MeXbP9OCAIBGtwZDlEs6YlE0Um/cFytqi7d+KzB3qqp+OEFIIYA7lgExREXBCCIDHv6hcjZ2U3h5jLk9Jxo+WX2hJ0f8ATvxL0cTEe2d77tq+NA4LWVygWPh9kchKs5D9qVHKTiK+U=~-1~-1~-1",
    "_cls_s":	"83163b84-2088-4dce-b68c-dc371616079d:0",
    "_cls_v":	"9da0bcf3-1541-4815-b22b-6738aa4b3584",
    "_taggstar_exp":	"v:3|id:|group:",
    "_taggstar_ses":	"1cdf0ba0-fd8d-11ee-93d8-0f708df9eed2",
    "_taggstar_vid":	"2dca6491-d708-11ee-8214-537a6449f81f",
    "ak_bmsc":	"32DD290A670BE5ABD4ED0EDEEBED8934~000000000000000000000000000000~YAAQj3nKF79bfOWOAQAA1TCJ8RfMxWvXOpBKOBRY7HfBgBK1NzQQ+OXr9jtBeAJWLi0Zlh/Rt33oNkFGlliI8A34jFq/LPRc4Ni47Pg3lYZoShVqwjcWRdRskGwAALV4xgAwvMOcKV4lQOeRI+nxinV61ipI5am+PUGS///WeCFdNXm6ubI8EgFy10z/K7L1+jgwS4mi8J44UrDSRR8AZfELO9SMC01kXNqPKCrfdN2UJCKqKOSqfqGJydazOr4dwV0TZvcwgOINXMkfSd0QNLqwc2kci6VnoyVFOO9DCml+rpVexo7Nkk9qeESp3nH0+5xSPpali17ZFqVs6c+lGApn0naP46DtdY/BDIK/CmBCXLojJyHy4gWrkGqlAkHcaqKK9qHFCYyI4uU=",
    "AKA_A2":	"A",
    "akaas_arg_uk_global":	"1714658906~rv=56~id=92a5ec062ebd239e33205dce68700204",
    "akavpau_vpc_gcd":	"1709744329~id=61190d81c53eb6701ea7850ecac2d81c",
    "akavpau_vpc_pdpcd":	"1713449905~id=8b2233f1328bd5f31cd4543e85590fb5",
    "AMCV_095C467352782EB30A490D45@AdobeOrg":	"179643557|MCIDTS|19832|MCMID|87286231597634338936380337387751060019|MCAID|NONE|MCOPTOUT-1713456507s|NONE|vVersion|5.5.0",
    "AMCVS_095C467352782EB30A490D45@AdobeOrg":	"1",
    "analytics_channel":	"ecomm",
    "ArgosPopUp_customer1In20Chance":	"false",
    "Bc":	"d:1*1_p:0*0.005_r:null*null",
    "bm_mi":	"F9C3C54D5DEA003C68C3FAF61043552C~YAAQj3nKF/ddfOWOAQAAqIaJ8Rfnd3kBiQAmJehQivTJIybpKGiuGoEXuXs2mf8/iym6lIqH+U1qCsOMWXk9EcLFaJHkcVjwA70AgQRrZ8B8bBXRr2pv9zBYAzGoh6rBEZywpYS5s3IikUI+tIHHLS25cM+xW78JYDOGNbqsNMNtBKkPD51PtPktxwrhP/tuTu78oStgsugrbDvbxmko01ucaVvtOIvpxbk8ZUAE4t7symTOVpMDIBLvLq2Iq6zd+KPHdw6qwfqczEnsBpXIeyOQWlFKcUNK4zyxokm0pyWNM3XpWB8crnUKI7Fyn9tAko/n+Qr+Bh44PiF7RqU=~1",
    "bm_sv":	"7CA6284BBE739191EA1137E812E7367F~YAAQj3nKFzJffOWOAQAAL6KJ8RdCwAVCEU3dXh7rSuaAmuzFrpoiHR9Ubdy1u4KhO8E0MurDMIb7M6QUtnU/NJN4CGmQEtshCV6cKX1v5jJ8OGeMWxgEr6ka5q0DjNKrkcRbqP75ea6H243pPpn8Dv14jSBwAci5YNVsVrTyYWJn59lALJLiyijOagRZ14mFqd6yFxLFkpdk2tnOyyTOrnT0S4peIJz6BVhNCJCkz6gQobJLVZ2Nhq80+Va4+F+roFg=~1",
    "bm_sz":	"5936C33442C479834E85E26858B9E983~YAAQj3nKF/ldfOWOAQAAqIaJ8RfeKpHldkDzhpzg/ll8RNX9aoRY7tHaj6vVwhlWZFqh2EbfACDAf1hLzDmlZyC7EZewquN2qkRRF9dRN21ZUCjNYIZlKWkm7GEu6Kyk0+MpHNpY5EDCxnYApM8x4lX7y6Br/CmjPjjthYQen0tlzw5KI/eJmdDAprbXFm+Ri0+mhfixEyFD9XHouo66T68HSjlaBb96vxAjx3G+nF0alYlKdJvGHDi0vsywQcCNRFeKpcguInhEBIhf6NkjHCXmYfN/ZlIbd4gjb2gADSUpm+OvgaNZqOevkYpq4/+h2cWRbzz9jthzNcGv96cpM7GBQRqzCK7IiucFOj5GiCqsVbMgraIISPDEkHmImqqORWzIdQ+e5bUWul8L0nuR2JWFA99M~3617605~4534597",
    "Checkout_Test_Group_2":	"NEW_HD|NEW_HD_SI|NEW_HD_LI",
    "cisId":	"1d7c61fafda24e0a8ae31dd19883dc18",
    "CONSENTMGR":	"consent:true|ts:1708004268257|id:018dacfc0c9c004ff4950a12766c05050005700d00bd0",
    "localisationTooltip":	"open",
    "mdr_browser":	"Akamai",
    "prev_vals":	"ar:pdp:7923726:hugobossthescentformeneaudetoilette-50ml:*|*ar:productdetails:",
    "sessionId":	"I3D82BBqnKS767BeIxicKX7TsVC0ChWsH5DyemS/TVOpxxZQzQdkHohf+9nW1V+/",
    "stimgs":	'{"sessionId":41478931,"didReportCameraImpression":false,"newUser":true}',
    "syte_uuid":	"20b4f410-fd8d-11ee-829e-9557f3b9dbbe",
    "ufvd":	"~~clp_29351-e!events_easter-gifts-U!clp_29203-o!clp_29949-Bk!clp_30299-U!brands_hugo-boss-K",
    "umdid":	"NDZmZDA1NTEtZjViYS00ZDlhLTkwYzEtMGEwZTY4N2I1M2YwfDdmZjZiYWFlLTIzZDItNDllZS1hNGQ3LWRmNWE4NDEyYmY5OXww",
    "utag_main":	"v_id:018dacfc0c9c004ff4950a12766c05050005700d00bd0$_sn:7$_se:28$_ss:0$_st:1713451123084$vapi_domain:argos.co.uk$dc_visit:7$ses_id:1713449286563;exp-session$_pn:2;exp-session$dc_event:24;exp-session"
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
            link = "https://www.argos.co.uk" + item.find('a', class_='ProductCardstyles__Link-h52kot-13')['href']

            item_data = {
                "name": name,
                "price": price,
                "link": link,
                "old_price": old_price
            }
            if link in prices:
                item_data["old_price"] = prices[link]["old_price"]
                if prices[link]["old_price"] > price and price != prices[link]["price"] and link not in temporary_discounts:
                    item_data["old_price"] = prices[link]["old_price"]
                    prices[link]["previous_price"] = prices[link]["price"]
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
        print("Failed to retrieve the page")
        return []


def get_keepa_results(price_drops):
    keepa_drops = []
    for price_drop in price_drops:
        if price_drop["old_price"] == 0 or price_drop["price"]/price_drop["previous_price"] <= 0.85:
            bar_code = get_bar_code(price_drop["link"])
            if not bar_code:
                continue

            compare_price, fee, fee_percentage = keepa_manager.get_from_bar_code(bar_code)
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
                    "margin": profit_margin
                }
                print(margin_ping)
                keepa_drops.append(margin_ping)
    return keepa_drops


def get_bar_code(link):
    response = requests.get(link, headers=header, cookies=cookies)
    soup = BeautifulSoup(response.content, 'html.parser')
    description = soup.find("div", class_="product-description-content-text")
    lines = description.find_all("li")
    if len(lines) > 0 and "EAN:" in lines[len(lines)-1].text:
        return lines[len(lines)-1].text.replace("EAN:", "").replace(".", "").strip()
    return None


