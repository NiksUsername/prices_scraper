from datetime import datetime, timedelta

import argos_scraper
import coolshop_scraper
import currys_scraper
import dell_scraper
import game_co_scraper
import discord
import asyncio

import houseoffraser_scraper
import johnlewis_scraper
import laptopsdirect_scraper
import ryman_scraper
import selfridges_scraper
from config import *
from database_manager import write_data_to_db
from discount_properties import is_big_discount
from links import *

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True
intents.message_content = True
client = discord.Client(intents=intents)

game_channel_id = 1209922009824239666
argos_channel_id = 1215250546295050260
laptops_direct_channel_id = 1216395055514783795
john_lewis_channel_id = 1216394889567141940
currys_channel_id = 1216395018697310239
houseoffraser_channel_id = 1223789428271485048
dell_channel_id = 1223789521674567810
coolshop_channel_id = 1223789470294478878
selfridges_channel_id = 1223789398513160194
ryman_channel_id = 1223789490737381459

game_unfiltered_id = 1228366296886939679
argos_unfiltered_id = 1228366712437735435
laptops_direct_unfiltered_id = 1228366867048042496
john_lewis_unfiltered_id = 1228366786747957370
currys_unfiltered_id = 1228366819312664658
houseoffraser_unfiltered_id = 1228366956436914447
dell_unfiltered_id = 1228367049227636810
coolshop_unfiltered_id = 1228366991803285504
selfridges_unfiltered_id = 1228366906117984428
ryman_unfiltered_id = 1228367022958575636

argos_keepa_id = 1230501172633276496
ryman_keepa_id = 1230501232674865214


def get_laptops_update(url):
    prices = laptopsdirect_scraper.get_new_prices(url)
    return get_updates(prices, "www.laptopsdirect.co.uk")


def get_johnlewis_update(url):
    prices = johnlewis_scraper.get_new_prices(url)
    return get_updates(prices, "www.johnlewis.com")


def get_argos_update(url, check_keepa=True):
    prices = argos_scraper.get_new_prices(url)
    if check_keepa:
        keepa_updates = get_keepa_difference(argos_scraper.get_keepa_results(prices), "www.ryman.co.uk")
    else:
        keepa_updates = []
    site_updates = get_updates(prices, "www.ryman.co.uk")
    return site_updates + (keepa_updates,)


def get_games_update(url):
    prices = game_co_scraper.get_new_prices(url+"?contentOnly=&inStockOnly=true&listerOnly=&pageSize=600&sortBy=MOST_POPULAR_DESC&pageNumber=1")
    return get_updates(prices, "www.game.co.uk")


def get_currys_update(url):
    prices = currys_scraper.get_new_prices(url)
    return get_updates(prices, "www.currys.co.uk")


def get_houseoffraser_update(url):
    prices = houseoffraser_scraper.get_new_prices(url)
    return get_updates(prices, "www.houseoffraser.co.uk")


def get_selfridges_update(url):
    prices = selfridges_scraper.get_new_prices(url)
    return get_updates(prices, "www.selfridges.com")


def get_dell_update(url):
    prices = dell_scraper.get_new_prices(url)
    return get_updates(prices, "www.dell.com")


def get_ryman_update(url, check_keepa=True):
    prices = ryman_scraper.get_new_prices(url)
    if check_keepa: keepa_updates = get_keepa_difference(ryman_scraper.get_keepa_results(prices), "www.argos.co.uk")
    else: keepa_updates = []
    site_updates = get_updates(prices, "www.argos.co.uk")
    return site_updates + (keepa_updates,)


def get_coolshop_update(url):
    prices = coolshop_scraper.get_new_prices(url)
    return get_updates(prices, "www.coolshop.co.uk")


def get_updates(prices, website):
    messages = []
    unfiltered = []
    for price in prices:
        if price["old_price"] == 0:
            continue
            #old_price = "n/a"
            #change = "n/a"
        else:
            old_price = f"£{round(price['old_price'], 2)}"
            change = str(round((price["old_price"] - price["price"]) / price["old_price"] * 100)) + "%"
        print(price)
        link_name = price["name"].replace(" ", "%20").replace("\xa0", "%20")
        mobile_name = link_name.split("%20")
        words_size = min(len(mobile_name), 5)
        mobile_name = "%20".join(mobile_name[0:words_size])
        embed = discord.Embed(
            title=f"{price['name']}",
            description=f"New Price - £{price['price']} \n" \
                        f"Old Price - {old_price} \n" \
                        f"Change - {change} \n\n"
                        f"Website link: \n" \
                        f"[{website}]({price['link']}) \n"
                        f"\nLinks: \n"
                        f"[Amazon](https://www.amazon.co.uk/s?k={link_name}) | "
                        f"[Keepa](https://keepa.com/#!search/2-{link_name}) | "
                        f"[SellerAmp](https://sas.selleramp.com/sas/lookup?SasLookup&search_term={link_name}) | "
                        f"[SellerAmp(Mobile)](https://sas.selleramp.com/sas/lookup?SasLookup&search_term={mobile_name})\n",
            color=0x0000ff
        )
        if is_big_discount(price):
            messages.append(embed)
        else:
            unfiltered.append(embed)
    return messages, unfiltered


def get_keepa_difference(prices, website):
    messages = []
    for price in prices:
        keepa_price = f"£{round(price['keepa_price'], 2)}"
        margin = str(round((price["margin"] * 100)) + "%")
        print(price)
        link_name = price["name"].replace(" ", "%20").replace("\xa0", "%20")
        mobile_name = link_name.split("%20")
        words_size = min(len(mobile_name), 5)
        mobile_name = "%20".join(mobile_name[0:words_size])
        embed = discord.Embed(
            title=f"{price['name']}",
            description=f"Price - £{price['price']} \n" \
                        f"Keepa Price - {keepa_price} \n" \
                        f"Margin - {margin} \n\n"
                        f"Website link: \n" \
                        f"[{website}]({price['link']}) \n"
                        f"\nLinks: \n"
                        f"[Amazon](https://www.amazon.co.uk/s?k={link_name}) | "
                        f"[Keepa](https://keepa.com/#!search/2-{link_name}) | "
                        f"[SellerAmp](https://sas.selleramp.com/sas/lookup?SasLookup&search_term={link_name}) | "
                        f"[SellerAmp(Mobile)](https://sas.selleramp.com/sas/lookup?SasLookup&search_term={mobile_name})\n",
            color=0x0000ff
        )
        messages.append(embed)
    return messages


async def send_game_notification():
    await client.wait_until_ready()
    selected_channel = client.get_channel(game_channel_id)
    unfiltered_channel = client.get_channel(game_unfiltered_id)
    curr_time = datetime.now()
    if selected_channel is None:
        print("Error: Channel not found.")
        return
    while not client.is_closed():
        try:
            selected_channel = client.get_channel(game_channel_id)
            for link in game_links:
                try:
                    return_value, unfiltered_value = await asyncio.to_thread(get_games_update, link)
                except Exception as e:
                    print(e.with_traceback)
                    print("game")
                    continue
                if return_value:
                    for i in return_value:
                        await selected_channel.send(embed=i)
                if unfiltered_value:
                    for i in unfiltered_value:
                        await unfiltered_channel.send(embed=i)
                await asyncio.sleep(1)
            delta = datetime.now() - curr_time
            now = datetime.now()
            delay = 300
            if 2 < now.hour < 13:
                delay = 60
            await asyncio.sleep(max(delay - delta.total_seconds(), 0))
            curr_time = now
            game_co_scraper.first_run = False
        except Exception:
            print("Major Game Exception")


async def send_argos_notification():
    await client.wait_until_ready()
    selected_channel = client.get_channel(argos_channel_id)
    unfiltered_channel = client.get_channel(argos_unfiltered_id)
    keepa_channel = client.get_channel(argos_keepa_id)
    curr_time = datetime.now()
    if selected_channel is None:
        print("Error: Channel not found.")
        return
    for link in argos_links:
        await asyncio.sleep(1)
        await asyncio.to_thread(get_argos_update, link, False)
    while not client.is_closed():
        try:
            selected_channel = client.get_channel(argos_channel_id)
            for link in argos_links:
                try:
                    return_value, unfiltered_value, keepa_value = await asyncio.to_thread(get_argos_update, link, True)
                except Exception as e:
                    print(e.with_traceback)
                    print("argos")
                    continue
                if return_value:
                    for i in return_value:
                        await selected_channel.send(embed=i)
                if unfiltered_value:
                    for i in unfiltered_value:
                        await unfiltered_channel.send(embed=i)
                if keepa_value:
                    for i in keepa_value:
                        await keepa_channel.send(embed=i)
                await asyncio.sleep(1)
            delta = datetime.now() - curr_time
            now = datetime.now()
            delay = 300
            if 4 < now.hour < 8:
                delay = 60
            await asyncio.sleep(max(delay - delta.total_seconds(), 0))
            curr_time = now
        except Exception:
            print("Major Argos Exception")


async def send_laptops_notification():
    await client.wait_until_ready()
    selected_channel = client.get_channel(laptops_direct_channel_id)
    unfiltered_channel = client.get_channel(laptops_direct_unfiltered_id)
    curr_time = datetime.now()
    if selected_channel is None:
        print("Error: Channel not found.")
        return
    for link in laptops_direct_links:
        await asyncio.sleep(1)
        await asyncio.to_thread(get_laptops_update, link)
    while not client.is_closed():
        try:
            selected_channel = client.get_channel(laptops_direct_channel_id)
            for link in laptops_direct_links:
                try:
                    return_value, unfiltered_value = await asyncio.to_thread(get_laptops_update, link)
                except Exception as e:
                    print(e.with_traceback)
                    continue
                if return_value:
                    for i in return_value:
                        await selected_channel.send(embed=i)
                if unfiltered_value:
                    for i in unfiltered_value:
                        await unfiltered_channel.send(embed=i)
                await asyncio.sleep(1)
            delta = datetime.now() - curr_time
            await asyncio.sleep(max(300 - delta.total_seconds(), 0))
            curr_time = curr_time + timedelta(seconds=300)
        except Exception:
            print("Major Laptops Exception")


async def send_johnlewis_notification():
    await client.wait_until_ready()
    selected_channel = client.get_channel(john_lewis_channel_id)
    unfiltered_channel = client.get_channel(john_lewis_unfiltered_id)
    curr_time = datetime.now()
    if selected_channel is None:
        print("Error: Channel not found.")
        return
    for link in john_lewis_links:
        await asyncio.sleep(1)
        await asyncio.to_thread(get_johnlewis_update, link)
    while not client.is_closed():
        try:
            selected_channel = client.get_channel(john_lewis_channel_id)
            for link in john_lewis_links:
                try:
                    return_value, unfiltered_value = await asyncio.to_thread(get_johnlewis_update, link)
                except Exception as e:
                    print(e.with_traceback)
                    continue
                if return_value:
                    for i in return_value:
                        await selected_channel.send(embed=i)
                if unfiltered_value:
                    for i in unfiltered_value:
                        await unfiltered_channel.send(embed=i)
                await asyncio.sleep(1)
            delta = datetime.now() - curr_time
            now = datetime.now()
            delay = 300
            if now.hour < 3:
                delay = 60
            await asyncio.sleep(max(delay - delta.total_seconds(), 0))
            curr_time = now
        except Exception:
            print("Major John Lewis Exception")


async def send_currys_notification():
    await client.wait_until_ready()
    selected_channel = client.get_channel(currys_channel_id)
    unfiltered_channel = client.get_channel(currys_unfiltered_id)
    curr_time = datetime.now()
    if selected_channel is None:
        print("Error: Channel not found.")
        return
    for link in currys_links:
        await asyncio.sleep(0.5)
        await asyncio.to_thread(get_currys_update, link)
    while not client.is_closed():
        try:
            selected_channel = client.get_channel(currys_channel_id)
            for link in currys_links:
                try:
                    return_value, unfiltered_value = await asyncio.to_thread(get_currys_update, link)
                except Exception as e:
                    print(e.with_traceback)
                    continue
                if return_value:
                    for i in return_value:
                        await selected_channel.send(embed=i)
                if unfiltered_value:
                    for i in unfiltered_value:
                        await unfiltered_channel.send(embed=i)
                await asyncio.sleep(0.5)
            delta = datetime.now() - curr_time
            await asyncio.sleep(max(300 - delta.total_seconds(), 0))
            curr_time = curr_time + timedelta(seconds=300)
        except Exception:
            print("Major John Lewis Exception")


async def send_houseoffraser_notification():
    await client.wait_until_ready()
    print("started")
    selected_channel = client.get_channel(houseoffraser_channel_id)
    unfiltered_channel = client.get_channel(houseoffraser_unfiltered_id)
    curr_time = datetime.now()
    if selected_channel is None:
        print("Error: Channel not found.")
        return
    for link in houseoffraser_links:
        await asyncio.sleep(0.5)
        await asyncio.to_thread(get_houseoffraser_update, link)
    while not client.is_closed():
        try:
            selected_channel = client.get_channel(houseoffraser_channel_id)
            for link in houseoffraser_links:
                try:
                    return_value, unfiltered_value = await asyncio.to_thread(get_houseoffraser_update, link)
                except Exception as e:
                    print(e.with_traceback)
                    continue
                if return_value:
                    for i in return_value:
                        await selected_channel.send(embed=i)
                if unfiltered_value:
                    for i in unfiltered_value:
                        await unfiltered_channel.send(embed=i)
                await asyncio.sleep(0.5)
            delta = datetime.now() - curr_time
            await asyncio.sleep(max(60 - delta.total_seconds(), 0))
            curr_time = curr_time + timedelta(seconds=300)
        except Exception:
            print("Major house of fraser Exception")


async def send_selfridges_notification():
    await client.wait_until_ready()
    selected_channel = client.get_channel(selfridges_channel_id)
    unfiltered_channel = client.get_channel(selfridges_unfiltered_id)
    curr_time = datetime.now()
    if selected_channel is None:
        print("Error: Channel not found.")
        return
    for link in selfridges_links:
        await asyncio.sleep(2)
        await asyncio.to_thread(get_selfridges_update, link)
    while not client.is_closed():
        try:
            selected_channel = client.get_channel(selfridges_channel_id)
            for link in selfridges_links:
                try:
                    return_value, unfiltered_value = await asyncio.to_thread(get_selfridges_update, link)
                except Exception as e:
                    print(e.with_traceback)
                    continue
                if return_value:
                    for i in return_value:
                        await selected_channel.send(embed=i)
                if unfiltered_value:
                    for i in unfiltered_value:
                        await unfiltered_channel.send(embed=i)
                await asyncio.sleep(3)
            delta = datetime.now() - curr_time
            await asyncio.sleep(max(900 - delta.total_seconds(), 0))
            curr_time = curr_time + timedelta(seconds=900)
        except Exception:
            print("Major Selfridges Exception")


async def send_dell_notification():
    await client.wait_until_ready()
    selected_channel = client.get_channel(dell_channel_id)
    unfiltered_channel = client.get_channel(dell_unfiltered_id)
    curr_time = datetime.now()
    if selected_channel is None:
        print("Error: Channel not found.")
        return
    for link in dell_links:
        await asyncio.sleep(0.5)
        await asyncio.to_thread(get_dell_update, link)
    while not client.is_closed():
        try:
            selected_channel = client.get_channel(dell_channel_id)
            for link in dell_links:
                try:
                    return_value, unfiltered_value = await asyncio.to_thread(get_dell_update, link)
                except Exception as e:
                    print(e.with_traceback)
                    continue
                if return_value:
                    for i in return_value:
                        await selected_channel.send(embed=i)
                if unfiltered_value:
                    for i in unfiltered_value:
                        await unfiltered_channel.send(embed=i)
                await asyncio.sleep(0.5)
            delta = datetime.now() - curr_time
            await asyncio.sleep(max(300 - delta.total_seconds(), 0))
            curr_time = curr_time + timedelta(seconds=300)
        except Exception:
            print("Major Dell Exception")


async def send_ryman_notification():
    await client.wait_until_ready()
    selected_channel = client.get_channel(ryman_channel_id)
    unfiltered_channel = client.get_channel(ryman_unfiltered_id)
    keepa_channel = client.get_channel(ryman_keepa_id)
    curr_time = datetime.now()
    if selected_channel is None:
        print("Error: Channel not found.")
        return
    for link in ryman_links:
        await asyncio.sleep(0.5)
        await asyncio.to_thread(get_ryman_update, link, False)
    while not client.is_closed():
        try:
            selected_channel = client.get_channel(ryman_channel_id)
            for link in ryman_links:
                try:
                    return_value, unfiltered_value, keepa_value = await asyncio.to_thread(get_ryman_update, link, True)
                except Exception as e:
                    print(e.with_traceback)
                    continue
                if return_value:
                    for i in return_value:
                        await selected_channel.send(embed=i)
                if unfiltered_value:
                    for i in unfiltered_value:
                        await unfiltered_channel.send(embed=i)
                if keepa_value:
                    for i in keepa_value:
                        await keepa_channel.send(embed=i)
                await asyncio.sleep(0.5)
            delta = datetime.now() - curr_time
            await asyncio.sleep(max(300 - delta.total_seconds(), 0))
            curr_time = curr_time + timedelta(seconds=300)
        except Exception:
            print("Major Ryman Exception")


async def send_coolshop_notification():
    await client.wait_until_ready()
    selected_channel = client.get_channel(coolshop_channel_id)
    unfiltered_channel = client.get_channel(coolshop_unfiltered_id)
    curr_time = datetime.now()
    if selected_channel is None:
        print("Error: Channel not found.")
        return
    for link in coolshop_links:
        await asyncio.sleep(0.5)
        await asyncio.to_thread(get_coolshop_update, link)
    while not client.is_closed():
        try:
            selected_channel = client.get_channel(coolshop_channel_id)
            for link in coolshop_links:
                try:
                    return_value, unfiltered_value = await asyncio.to_thread(get_coolshop_update, link)
                except Exception as e:
                    print(e.with_traceback)
                    continue
                if return_value:
                    for i in return_value:
                        await selected_channel.send(embed=i)
                if unfiltered_value:
                    for i in unfiltered_value:
                        await unfiltered_channel.send(embed=i)
                await asyncio.sleep(0.5)
            delta = datetime.now() - curr_time
            await asyncio.sleep(max(300 - delta.total_seconds(), 0))
            curr_time = curr_time + timedelta(seconds=300)
        except Exception:
            print("Major Coolshop Exception")


# Event: Bot is ready
@client.event
async def on_ready():
    print('Logged in as', client.user.name)
    print('------')
    await asyncio.gather(
        send_game_notification(),
        send_laptops_notification(),
        send_argos_notification(),
        send_currys_notification(),
        send_johnlewis_notification(),
        send_houseoffraser_notification(),
        send_ryman_notification(),
        send_dell_notification(),
        send_selfridges_notification(),
        send_coolshop_notification()
    )


# Event: Message received
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    global game_channel_id
    if message.content.startswith('!set_channel') and (message.guild is not None) and (message.guild.owner == message.author):
        game_channel_id = message.channel.id
        print(game_channel_id)
        await message.channel.send(f"Channel successfully set")
    elif message.content.startswith("!force_ping") and (message.guild is not None) and (message.guild.owner == message.author):
        url = message.content.replace("!force_ping", "").strip()
        ping = ""
        if "www.game.co.uk" in url:
            ping = game_co_scraper.prices.get(url)
        elif "www.argos.co.uk" in url:
            ping = argos_scraper.prices.get(url)
        elif "www.laptopsdirect.co.uk" in url:
            ping = laptopsdirect_scraper.prices.get(url)
        elif "www.johnlewis.com" in url:
            ping = johnlewis_scraper.prices.get(url)
        elif "www.currys.co.uk" in url:
            ping = currys_scraper.prices.get(url)
        elif "www.houseoffraser.co.uk" in url:
            ping = houseoffraser_scraper.prices.get(url)
        elif "www.coolshop.co.uk" in url:
            ping = coolshop_scraper.prices.get(url)
        elif "www.dell.com" in url:
            ping = dell_scraper.prices.get(url)
        elif "www.ryman.co.uk" in url:
            ping = ryman_scraper.prices.get(url)
        elif "www.selfridges.com" in url:
            ping = selfridges_scraper.prices.get(url)
        if ping:
            print(ping)
            ping_embed = get_updates([ping], "Force Ping")[0]
            if ping_embed:
                await message.channel.send(embed=ping_embed)
            else:
                await message.channel.send("Failed to find item by this url.")
        else:
            await message.channel.send("Failed to retrieve. Wrong url.")



loop = asyncio.get_event_loop()


async def run_bot():
    try:
        await client.start(TOKEN)
    except:
        await client.close()
    finally:
        write_data_to_db(argos_scraper.prices, "argos")
        write_data_to_db(coolshop_scraper.prices, "coolshop")
        write_data_to_db(currys_scraper.prices, "currys")
        write_data_to_db(dell_scraper.prices, "dell")
        write_data_to_db(houseoffraser_scraper.prices, "houseoffraser")
        write_data_to_db(game_co_scraper.prices, "game")
        write_data_to_db(johnlewis_scraper.prices, "john_lewis")
        write_data_to_db(laptopsdirect_scraper.prices, "laptops_direct")
        write_data_to_db(ryman_scraper.prices, "ryman")
        write_data_to_db(selfridges_scraper.prices, "selfridges")



async def main():
    print("Starting gather")
    await asyncio.gather(
        run_bot()
    )


loop.run_until_complete(main())

