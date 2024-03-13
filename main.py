from datetime import datetime, timedelta

import argos_scraper
import currys_scraper
import game_co_scraper
import discord
import asyncio

import johnlewis_scraper
import laptopsdirect_scraper
from config import *
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


def get_laptops_update(url):
    prices = laptopsdirect_scraper.get_new_prices(url)
    return get_updates(prices, "www.laptopsdirect.co.uk")


def get_johnlewis_update(url):
    prices = johnlewis_scraper.get_new_prices(url)
    return get_updates(prices, "www.johnlewis.com")


def get_argos_update(url):
    prices = argos_scraper.get_new_prices(url)
    return get_updates(prices, "www.argos.co.uk")


def get_games_update(url):
    prices = game_co_scraper.get_new_prices(url+"?contentOnly=&inStockOnly=true&listerOnly=&pageSize=600&sortBy=MOST_POPULAR_DESC&pageNumber=1")
    return get_updates(prices, "www.game.co.uk")


def get_currys_update(url):
    prices = currys_scraper.get_new_prices(url)
    return get_updates(prices, "www.currys.co.uk")


def get_updates(prices, website):
    messages = []
    for price in prices:
        if price["old_price"] == 0:
            old_price = "n/a"
            change = "n/a"
        else:
            old_price = f"£{price['old_price']}"
            change = str(round((price["old_price"] - price["price"]) / price["old_price"] * 100)) + "%"
        print(price)
        link_name = price["name"].replace(" ", "%20")
        embed = discord.Embed(
            title=f"{price['name']}",
            description=f"New Price - £{price['price']} \n" \
                        f"Old Price - {old_price} \n" \
                        f"Change - {change} \n\n"
                        f"Website link: \n" \
                        f"[{website}]({price['link']}) \n"
                        f"\nLinks: \n"
                        f"[Amazon](https://www.amazon.co.uk/s?k={link_name}) | "
                        f"[Keepa](https://keepa.com/#!search/1-{link_name}) | "
                        f"[SellerAmp](https://sas.selleramp.com/sas/lookup?SasLookup&search_term={link_name})\n",
            color=0x0000ff
        )
        messages.append(embed)
    return messages


async def send_game_notification():
    await client.wait_until_ready()
    selected_channel = client.get_channel(game_channel_id)
    curr_time = datetime.now()
    if selected_channel is None:
        print("Error: Channel not found.")
        return
    while not client.is_closed():
        try:
            selected_channel = client.get_channel(game_channel_id)
            for link in game_links:
                try:
                    return_value = await asyncio.to_thread(get_games_update, link)
                except Exception as e:
                    print(e.with_traceback)
                    print("game")
                    continue
                if return_value:
                    for i in return_value:
                        await selected_channel.send(embed=i)
                await asyncio.sleep(1)
            delta = datetime.now() - curr_time
            await asyncio.sleep(max(60 - delta.total_seconds(), 0))
            curr_time = curr_time + timedelta(seconds=60)
            game_co_scraper.first_run = False
        except Exception:
            print("Major Game Exception")


async def send_argos_notification():
    await client.wait_until_ready()
    selected_channel = client.get_channel(argos_channel_id)
    curr_time = datetime.now()
    if selected_channel is None:
        print("Error: Channel not found.")
        return
    for link in argos_links:
        await asyncio.sleep(1)
        await asyncio.to_thread(get_argos_update, link)
    while not client.is_closed():
        try:
            selected_channel = client.get_channel(argos_channel_id)
            for link in argos_links:
                try:
                    return_value = await asyncio.to_thread(get_argos_update, link)
                except Exception as e:
                    print(e.with_traceback)
                    print("argos")
                    continue
                if return_value:
                    for i in return_value:
                        await selected_channel.send(embed=i)
                await asyncio.sleep(1)
            delta = datetime.now() - curr_time
            await asyncio.sleep(max(60 - delta.total_seconds(), 0))
            curr_time = curr_time + timedelta(seconds=60)
        except Exception:
            print("Major Argos Exception")


async def send_laptops_notification():
    await client.wait_until_ready()
    selected_channel = client.get_channel(laptops_direct_channel_id)
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
                    return_value = await asyncio.to_thread(get_laptops_update, link)
                except Exception as e:
                    print(e.with_traceback)
                    continue
                if return_value:
                    for i in return_value:
                        await selected_channel.send(embed=i)
                await asyncio.sleep(1)
            delta = datetime.now() - curr_time
            await asyncio.sleep(max(60 - delta.total_seconds(), 0))
            curr_time = curr_time + timedelta(seconds=60)
        except Exception:
            print("Major Laptops Exception")


async def send_johnlewis_notification():
    await client.wait_until_ready()
    selected_channel = client.get_channel(john_lewis_channel_id)
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
                    return_value = await asyncio.to_thread(get_johnlewis_update, link)
                except Exception as e:
                    print(e.with_traceback)
                    continue
                if return_value:
                    for i in return_value:
                        await selected_channel.send(embed=i)
                await asyncio.sleep(1)
            delta = datetime.now() - curr_time
            await asyncio.sleep(max(60 - delta.total_seconds(), 0))
            curr_time = curr_time + timedelta(seconds=60)
        except Exception:
            print("Major John Lewis Exception")


async def send_currys_notification():
    await client.wait_until_ready()
    selected_channel = client.get_channel(currys_channel_id)
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
                    return_value = await asyncio.to_thread(get_currys_update, link)
                except Exception as e:
                    print(e.with_traceback)
                    continue
                if return_value:
                    for i in return_value:
                        await selected_channel.send(embed=i)
                await asyncio.sleep(0.5)
            delta = datetime.now() - curr_time
            await asyncio.sleep(max(60 - delta.total_seconds(), 0))
            curr_time = curr_time + timedelta(seconds=60)
        except Exception:
            print("Major John Lewis Exception")


# Event: Bot is ready
@client.event
async def on_ready():
    print('Logged in as', client.user.name)
    print('------')
    client.loop.create_task(send_game_notification())
    client.loop.create_task(send_argos_notification())
    client.loop.create_task(send_laptops_notification())
    client.loop.create_task(send_johnlewis_notification())
    client.loop.create_task(send_currys_notification())

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

client.run(TOKEN)

