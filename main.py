import discord
from magiceden import aiohttp, floor_price
from pyth import get_price, asyncio


TOKEN = "YOUR SECRET DISCORD TOKEN"
status = discord.Status.online
intents = discord.Intents.default()
client = discord.Client(intents=intents, status=status)


async def update_activity():
    while True:
        floor = await floor_price()
        solprice = await get_price()
        solprice_usd = floor * solprice
        activity = discord.Activity(type=discord.ActivityType.watching, name=f"Floor {floor} SOL | {solprice_usd:.0f}$")
        await client.change_presence(activity=activity)
        await asyncio.sleep(60)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    client.loop.create_task(update_activity())

client.run(TOKEN)
