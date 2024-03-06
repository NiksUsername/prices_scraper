from datetime import datetime, timedelta

import argos_scraper
import game_co_scraper
import discord
import asyncio

from config import *

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True
intents.message_content = True
client = discord.Client(intents=intents)

game_links = [
    'https://www.game.co.uk/en/brands/western-digital/',
    'https://www.game.co.uk/en/brands/trust/',
    'https://www.game.co.uk/en/brands/turtle-beach/',
    'https://www.game.co.uk/en/brands/thrustmaster/',
    'https://www.game.co.uk/en/brands/steelseries/',
    'https://www.game.co.uk/en/brands/sony/',
    'https://www.game.co.uk/en/accessories/seagate-game-drives/',
    'https://www.game.co.uk/en/brands/samsung/',
    'https://www.game.co.uk/en/brands/razer/',
    'https://www.game.co.uk/en/brands/philips-hue/',
    'https://www.game.co.uk/en/brands/pdp/',
    'https://www.game.co.uk/en/brands/msi/',
    'https://www.game.co.uk/en/brands/logitech/',
    'https://www.game.co.uk/en/brands/lego/',
    'https://www.game.co.uk/en/brands/hyperx/',
    'https://www.game.co.uk/en/brands/hewlett-packard/',
    'https://www.game.co.uk/en/brands/hot-wheels/',
    'https://www.game.co.uk/en/brands/hasbro/',
    'https://www.game.co.uk/en/brands/fitbit/',
    'https://www.game.co.uk/en/brands/disney/',
    'https://www.game.co.uk/en/brands/corsair/',
    'https://www.game.co.uk/en/brands/casio/',
    'https://www.game.co.uk/en/brands/barbie/',
    'https://www.game.co.uk/en/brands/asus/',
    'https://www.game.co.uk/en/brands/jbl/',
    'https://www.game.co.uk/en/toys/trading-cards/',
    'https://www.game.co.uk/en/toys/board-games/',
    'https://www.game.co.uk/en/toys/card-games/',
    'https://www.game.co.uk/en/playstation/consoles/',
    'https://www.game.co.uk/en/playstation/games/',
    'https://www.game.co.uk/en/playstation/accessories/',
    'https://www.game.co.uk/en/xbox/consoles/',
    'https://www.game.co.uk/en/xbox/games/',
    'https://www.game.co.uk/en/xbox/accessories/',
    'https://www.game.co.uk/en/nintendo/consoles/',
    'https://www.game.co.uk/en/nintendo/games/',
    'https://www.game.co.uk/en/nintendo/accessories/',
]

argos_links = [
    'https://www.argos.co.uk/browse/health-and-beauty/fragrance/aftershave/c:29283/',
    'https://www.argos.co.uk/browse/health-and-beauty/fragrance/perfume/c:29282/',
    'https://www.argos.co.uk/browse/technology/computer-accessories/webcams/c:30060/',
    'https://www.argos.co.uk/browse/technology/computer-accessories/projectors/c:30100/',
    'https://www.argos.co.uk/browse/technology/computer-accessories/psu/c:1043074/',
    'https://www.argos.co.uk/browse/technology/computer-accessories/pc-fans-and-coolers/c:1041490/',
    'https://www.argos.co.uk/browse/technology/computer-accessories/computer-motherboards/c:1041491/',
    'https://www.argos.co.uk/browse/technology/computer-accessories/computer-cases/c:1041489/',
    'https://www.argos.co.uk/browse/technology/computer-accessories/graphics-cards/c:1041488/',
    'https://www.argos.co.uk/browse/technology/computer-accessories/external-hard-drives/c:30073/',
    'https://www.argos.co.uk/browse/garden-and-diy/diy-power-tools/saws/c:29668/',
    'https://www.argos.co.uk/browse/garden-and-diy/diy-power-tools/angle-grinders/c:29669/',
    'https://www.argos.co.uk/browse/garden-and-diy/diy-power-tools/sanders/c:29666/',
    'https://www.argos.co.uk/browse/garden-and-diy/diy-power-tools/drills/c:29675/',
    'https://www.argos.co.uk/browse/toys/lego/c:30379/',
    'https://www.argos.co.uk/browse/toys/family-games/board-games/c:30423/',
    'https://www.argos.co.uk/browse/technology/video-games-and-consoles/nintendo-switch/nintendo-switch-games/c:30292/',
    'https://www.argos.co.uk/browse/technology/video-games-and-consoles/xbox-series/xbox-series-games/c:812426/',
    'https://www.argos.co.uk/browse/technology/video-games-and-consoles/xbox-one/xbox-one-games/c:30031/',
    'https://www.argos.co.uk/browse/technology/video-games-and-consoles/ps5/ps5-games/c:812420/',
    'https://www.argos.co.uk/browse/technology/video-games-and-consoles/ps4/ps4-games/c:30037/',
    'https://www.argos.co.uk/browse/technology/computer-accessories/external-hard-drives/c:30073/',
    'https://www.argos.co.uk/browse/technology/pc-monitors/c:30075/',
    'https://www.argos.co.uk/browse/technology/printers/c:30088/',
    'https://www.argos.co.uk/browse/technology/hi-fi-systems/c:30135/',
    'https://www.argos.co.uk/browse/technology/sound-bars/c:30123/',
]

channel_id = 1209922009824239666


def get_argos_update(url):
    prices = argos_scraper.get_new_prices(url)
    return get_updates(prices, "www.argos.co.uk")


def get_games_update(url):
    prices = game_co_scraper.get_new_prices(url+"?contentOnly=&inStockOnly=true&listerOnly=&pageSize=600&sortBy=MOST_POPULAR_DESC&pageNumber=1")
    return get_updates(prices, "www.game.co.uk")


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
    selected_channel = client.get_channel(channel_id)
    curr_time = datetime.now()
    if selected_channel is None:
        print("Error: Channel not found.")
        return
    while not client.is_closed():
        try:
            selected_channel = client.get_channel(channel_id)
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
    selected_channel = client.get_channel(channel_id)
    curr_time = datetime.now()
    if selected_channel is None:
        print("Error: Channel not found.")
        return
    for link in argos_links:
        await asyncio.sleep(1)
        await asyncio.to_thread(get_argos_update, link)
    while not client.is_closed():
        try:
            selected_channel = client.get_channel(channel_id)
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


# Event: Bot is ready
@client.event
async def on_ready():
    print('Logged in as', client.user.name)
    print('------')
    client.loop.create_task(send_game_notification())
    client.loop.create_task(send_argos_notification())

# Event: Message received
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    global channel_id
    if message.content.startswith('!set_channel') and (message.guild is not None) and (message.guild.owner == message.author):
        channel_id = message.channel.id
        print(channel_id)
        await message.channel.send(f"Channel successfully set")

client.run(TOKEN)

