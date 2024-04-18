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
    'Cookie': 'analytics_channel=ecomm; _abck=F00624B0353064CB97EE9E72FB0043F3~0~YAAQtjxRaAk91eWOAQAAYX0D8gseZCHT4OT7yNxT9a+Biqq8T+yOag0O5++K3aVR/zgJ2UCD0eFUPPokkcFBiY14nAzVhZxiZNkQKYyi8jrQKNhkdBH8z87GMspG266F68m4eBAyi6BLuImDXAMd/BX8mn9pfNupWBNGykulmA5j8nIQTBUsPBnYKh4WGmAHSNMDPwIDTZflyoDXP0sr3fxaorbTluYiwTo1lHT8jFneMJo31THEFenW5pMRn7oQ6PGloCThm01bAv8vJnQJbWX8TG3VU7O+a8mm6XseVtWjKIg6XLzosUe+J1msf12+v/tXcUn2GvvqB2Xy/ajXMcCnwzTR8LrO407+b5OsP1k7TUUWiIBZEQJtMcBpRpvzkLLeTbbCCTY19PS7sdawWXIxkZfj3hIHUYtJjaMdaOVjVifccA==~-1~-1~-1; utag_main=v_id:018dacfc0c9c004ff4950a12766c05050005700d00bd0$_sn:9$_se:38$_ss:0$_st:1713459242823$vapi_domain:argos.co.uk$dc_visit:9$ses_id:1713457156347%3Bexp-session$_pn:2%3Bexp-session$dc_event:24%3Bexp-session; sessionId=I3D82BBqnKS767BeIxicKX7TsVC0ChWsH5DyemS/TVOpxxZQzQdkHohf+9nW1V+/; cisId=72c47669513d488c99140ab37c637acd; CONSENTMGR=consent:true%7Cts:1708004268257%7Cid:018dacfc0c9c004ff4950a12766c05050005700d00bd0; AMCV_095C467352782EB30A490D45%40AdobeOrg=179643557%7CMCIDTS%7C19832%7CMCMID%7C87286231597634338936380337387751060019%7CMCAID%7CNONE%7CMCOPTOUT-1713464498s%7CNONE%7CvVersion%7C5.5.0; _cls_v=9da0bcf3-1541-4815-b22b-6738aa4b3584; _taggstar_vid=2dca6491-d708-11ee-8214-537a6449f81f; _taggstar_exp=v:3|id:|group:; akaas_arg_uk_global=1714666897~rv=56~id=c4c1f92fdae5cfedb64e12e99854232f; Checkout_Test_Group_2=NEW_HD|NEW_HD_SI|NEW_HD_LI; umdid=NDZmZDA1NTEtZjViYS00ZDlhLTkwYzEtMGEwZTY4N2I1M2YwfDdmZjZiYWFlLTIzZDItNDllZS1hNGQ3LWRmNWE4NDEyYmY5OXww; bm_sz=5936C33442C479834E85E26858B9E983~YAAQtjxRaEc71eWOAQAAjHQD8heZt0y6FnWleZN/0jLt+DBSv/v5Mi5U5jqeoaxtaAjWvOXvpXeb6JTEghVuhbH52mwpzu7l/MILRpf7/YWSFEz7tCLoGSz+ibmdXkY82H7YaDQ3EJSmeTWbC8qgUU1MXYWpYXIHMW2mK/USlqKfohzkjGOEEr5FCZsQtr1aRYDWpnN1r5aeuMqe+cF/RzhkP5aGdavl8A+5fyb2FmtXA7eof6pFfJNn7sKhkkWHy6OCDuYC2yj8uNgqRR83FyEMhrIC9ylBPP0MZMLfb0zmU5v/Bv/HjQuRfkiqruLf0Oc5c69uMG95BGDTZrIb00MhyNJ3AtkItu+pLNyPz0SbTunwsbkY+wwNh9iNX+SbLv5DnUbL4FzHTe1ATL+NwCBNA5bv7QelYayW8Avw/0TcbXQHHJRPhjnuqHc=~3617605~4534597; localisationTooltip=open; syte_uuid=20b4f410-fd8d-11ee-829e-9557f3b9dbbe; syte_ab_tests={}; prev_vals=ar%3Apdp%3A7923726%3Ahugobossthescentformeneaudetoilette-50ml%3A*%7C*ar%3Aproductdetails%3A; AMCVS_095C467352782EB30A490D45%40AdobeOrg=1; ArgosPopUp_customer1In20Chance=false; _cls_s=83163b84-2088-4dce-b68c-dc371616079d:0; Bc=d:1*1_p:0*0.005_r:null*null; ufvd=~~clp_29351-e!events_easter-gifts-U!clp_29203-Ba!clp_29949-Bk!clp_30299-U!brands_hugo-boss-o; akavpau_vpc_gcd=1709744329~id=61190d81c53eb6701ea7850ecac2d81c; akavpau_vpc_pdpcd=1713457896~id=7dc8d03ec51f5bf75da0ca24e464b059; mdr_browser=Akamai; AKA_A2=A; ak_bmsc=180DCFED347E43BB3359551A2E2BFD8A~000000000000000000000000000000~YAAQtjxRaL/91OWOAQAAbU0B8hfGXhrsy5udCjUIvR7hfVtD9oRVwdxh0aepJxqs+N7HjNK8zOPoGKA1qvydk1ToWEJUAXNt+DwD2jIQCLfr0I3qage30jJAEWxVmXQbO29NdGzuGhuTUXh02VMxpsCv3urOcr1FtCoBq3kBxthRi9t+O4OxYtxEn4gFVUeU1LKdc5DFLTG5y71k4zOPLHBjOqZzp/1SCGlHD5QpumLR3eplC3Hbi1vrTbaIuX39kkGnrqx8Uigdv+iUBhTRCykaf+U3fzO8vv7u1y0wcSFjMWYyiIs30tWHtylvdesMk8xCV2QfiHtgf/U3bhKy3jz+J1HKYKjgutmja5rscsm1Ex72V+TfwMERjQ8jyE2z1wSD+Kgche1/A84=; bm_sv=1A88EB5F35CAA4FFDFE2DADE5F88D01B~YAAQtjxRaEM+1eWOAQAAk4QD8hc91Ku8EMwyma96uJwuKFh8bOGhNiy/KbEnU2ink385U4N34kXtaolaC0nE49xd2rFSC7YlysLyDI3S41SaSXDQHn9QJWGe/KI9h5Z1U/cp8VzxeGNTOb9CUXBLzOlnXfVUwEQOQ4n2iPlE+o0LFw6Kd06ednmYxuOunnohiRITpMh521UfZFB16JjrLAfMTmPPGbuo2UtpLihs9xzBUXjHA9V0lMp/clzNCsIUlR4=~1; stimgs={%22sessionId%22:2494330%2C%22didReportCameraImpression%22:false%2C%22newUser%22:false}; _taggstar_ses=6927d85e-fd9f-11ee-83fc-0bc59435350c; bm_mi=D0E22F0045DE49091EDED3AB99A0C38A~YAAQtjxRaEU71eWOAQAAjHQD8hd+qtv1aMQu/0bIgGPcMKc9QLm4sk08S/m2PgR/HV5zFxpyWZjT7Imys87ffoQzXScBcoTgjw3JsAcc3Azko2TdkhpeiJOmUWBCpvRL5n0ev92CZLcLTiTeida85adFlHhB9jaEblB25eTMREcl+hJLUAypBLwj8NOgX1CyktA4V+waUIiY0P6Irs82p5fq2qeE30XofqhXCFezSYgnedskbumJA2BFnrPwXhILavgABMC6VO3sRobS0ZQy67yYcM2MMxGjs2Q7pkcRg0Ov5MwooU7h5eKl61ELtHGfSAt7a/N7TK9RjiDBQ4c=~1'
}

cookies = {
    "_abck":	"F00624B0353064CB97EE9E72FB0043F3~0~YAAQtjxRaAk91eWOAQAAYX0D8gseZCHT4OT7yNxT9a+Biqq8T+yOag0O5++K3aVR/zgJ2UCD0eFUPPokkcFBiY14nAzVhZxiZNkQKYyi8jrQKNhkdBH8z87GMspG266F68m4eBAyi6BLuImDXAMd/BX8mn9pfNupWBNGykulmA5j8nIQTBUsPBnYKh4WGmAHSNMDPwIDTZflyoDXP0sr3fxaorbTluYiwTo1lHT8jFneMJo31THEFenW5pMRn7oQ6PGloCThm01bAv8vJnQJbWX8TG3VU7O+a8mm6XseVtWjKIg6XLzosUe+J1msf12+v/tXcUn2GvvqB2Xy/ajXMcCnwzTR8LrO407+b5OsP1k7TUUWiIBZEQJtMcBpRpvzkLLeTbbCCTY19PS7sdawWXIxkZfj3hIHUYtJjaMdaOVjVifccA==~-1~-1~-1",
    "_cls_s":	"83163b84-2088-4dce-b68c-dc371616079d:0",
    "_cls_v":	"9da0bcf3-1541-4815-b22b-6738aa4b3584",
    "_taggstar_exp":	"v:3|id:|group:",
    "_taggstar_ses":	"6927d85e-fd9f-11ee-83fc-0bc59435350c",
    "_taggstar_vid":	"2dca6491-d708-11ee-8214-537a6449f81f",
    "ak_bmsc":	"180DCFED347E43BB3359551A2E2BFD8A~000000000000000000000000000000~YAAQtjxRaL/91OWOAQAAbU0B8hfGXhrsy5udCjUIvR7hfVtD9oRVwdxh0aepJxqs+N7HjNK8zOPoGKA1qvydk1ToWEJUAXNt+DwD2jIQCLfr0I3qage30jJAEWxVmXQbO29NdGzuGhuTUXh02VMxpsCv3urOcr1FtCoBq3kBxthRi9t+O4OxYtxEn4gFVUeU1LKdc5DFLTG5y71k4zOPLHBjOqZzp/1SCGlHD5QpumLR3eplC3Hbi1vrTbaIuX39kkGnrqx8Uigdv+iUBhTRCykaf+U3fzO8vv7u1y0wcSFjMWYyiIs30tWHtylvdesMk8xCV2QfiHtgf/U3bhKy3jz+J1HKYKjgutmja5rscsm1Ex72V+TfwMERjQ8jyE2z1wSD+Kgche1/A84=",
    "AKA_A2":	"A",
    "akaas_arg_uk_global":	"1714666897~rv=56~id=c4c1f92fdae5cfedb64e12e99854232f",
    "akavpau_vpc_gcd":	"1709744329~id=61190d81c53eb6701ea7850ecac2d81c",
    "akavpau_vpc_pdpcd":	"1713457896~id=7dc8d03ec51f5bf75da0ca24e464b059",
    "AMCV_095C467352782EB30A490D45@AdobeOrg":	"179643557|MCIDTS|19832|MCMID|87286231597634338936380337387751060019|MCAID|NONE|MCOPTOUT-1713464498s|NONE|vVersion|5.5.0",
    "AMCVS_095C467352782EB30A490D45@AdobeOrg":	"1",
    "analytics_channel":	"ecomm",
    "ArgosPopUp_customer1In20Chance":	"false",
    "Bc":	"d:1*1_p:0*0.005_r:null*null",
    "bm_mi":	"D0E22F0045DE49091EDED3AB99A0C38A~YAAQtjxRaEU71eWOAQAAjHQD8hd+qtv1aMQu/0bIgGPcMKc9QLm4sk08S/m2PgR/HV5zFxpyWZjT7Imys87ffoQzXScBcoTgjw3JsAcc3Azko2TdkhpeiJOmUWBCpvRL5n0ev92CZLcLTiTeida85adFlHhB9jaEblB25eTMREcl+hJLUAypBLwj8NOgX1CyktA4V+waUIiY0P6Irs82p5fq2qeE30XofqhXCFezSYgnedskbumJA2BFnrPwXhILavgABMC6VO3sRobS0ZQy67yYcM2MMxGjs2Q7pkcRg0Ov5MwooU7h5eKl61ELtHGfSAt7a/N7TK9RjiDBQ4c=~1",
    "bm_sv":	"1A88EB5F35CAA4FFDFE2DADE5F88D01B~YAAQtjxRaEM+1eWOAQAAk4QD8hc91Ku8EMwyma96uJwuKFh8bOGhNiy/KbEnU2ink385U4N34kXtaolaC0nE49xd2rFSC7YlysLyDI3S41SaSXDQHn9QJWGe/KI9h5Z1U/cp8VzxeGNTOb9CUXBLzOlnXfVUwEQOQ4n2iPlE+o0LFw6Kd06ednmYxuOunnohiRITpMh521UfZFB16JjrLAfMTmPPGbuo2UtpLihs9xzBUXjHA9V0lMp/clzNCsIUlR4=~1",
    "bm_sz":	"5936C33442C479834E85E26858B9E983~YAAQtjxRaEc71eWOAQAAjHQD8heZt0y6FnWleZN/0jLt+DBSv/v5Mi5U5jqeoaxtaAjWvOXvpXeb6JTEghVuhbH52mwpzu7l/MILRpf7/YWSFEz7tCLoGSz+ibmdXkY82H7YaDQ3EJSmeTWbC8qgUU1MXYWpYXIHMW2mK/USlqKfohzkjGOEEr5FCZsQtr1aRYDWpnN1r5aeuMqe+cF/RzhkP5aGdavl8A+5fyb2FmtXA7eof6pFfJNn7sKhkkWHy6OCDuYC2yj8uNgqRR83FyEMhrIC9ylBPP0MZMLfb0zmU5v/Bv/HjQuRfkiqruLf0Oc5c69uMG95BGDTZrIb00MhyNJ3AtkItu+pLNyPz0SbTunwsbkY+wwNh9iNX+SbLv5DnUbL4FzHTe1ATL+NwCBNA5bv7QelYayW8Avw/0TcbXQHHJRPhjnuqHc=~3617605~4534597",
    "Checkout_Test_Group_2":	"NEW_HD|NEW_HD_SI|NEW_HD_LI",
    "cisId":	"72c47669513d488c99140ab37c637acd",
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
                    "avg": avg90
                }
                print(margin_ping)
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


