from datetime import datetime, timedelta

from game_co_scraper import get_new_prices
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

channel_id = 1209922009824239666


def get_games_update(url):
    prices = get_new_prices(url+"?contentOnly=&inStockOnly=true&listerOnly=&pageSize=600&sortBy=MOST_POPULAR_DESC&pageNumber=1")
    messages = []
    for price in prices:
        change = round((price["old_price"]-price["price"])/price["old_price"]*100)
        print(price)
        link_name = price["name"].replace(" ", "%20")
        embed = discord.Embed(
            title=f"[{price['name']}]({price['link']})",
            description=f"New Price - £{price['price']} \n" \
                        f"Old Price - £{price['old_price']} \n" \
                        f"Change - {change}% \n" \
                        f"\nLinks: \n"
                        f"[Amazon](https://www.amazon.com/s?k={link_name}) | "
                        f"[Keepa](https://keepa.com/#!search/1-{link_name}) | "
                        f"[SellerAmp](https://sas.selleramp.com/sas/lookup?SasLookup&search_term={link_name})\n",
            color=0x0000ff
        )
        messages.append(embed)
    return messages


async def send_notification():
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
                    return_value = get_games_update(link)
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
            print("Major Exception")

# Event: Bot is ready
@client.event
async def on_ready():
    print('Logged in as', client.user.name)
    print('------')
    client.loop.create_task(send_notification())

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

