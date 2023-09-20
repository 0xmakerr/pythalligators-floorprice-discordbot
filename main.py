import discord
from discord.ext import commands, tasks
from magiceden import aiohttp, floor_price, unique_holders, listings, activities
from pyth import get_price, asyncio


TOKEN = ""
status = discord.Status.online
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def update_activity():
    while True:
        try:
            await activities()
            floor, listed_count, all_volume = await floor_price()
            solprice = await get_price()
            solprice_usd = floor * solprice
            activity = discord.Activity(type=discord.ActivityType.watching, name=f"Floor {floor} SOL | {solprice_usd:.0f}$")
            await bot.change_presence(activity=activity)
            await asyncio.sleep(60)
        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(60)


@bot.command()
async def gators(ctx):
    floor, listed_count, all_volume = await floor_price()
    num_of_unique_holders = await unique_holders()
    floor_listing, floor_img = await listings()
    last_sale, signature = await activities()
    # Create an embed object
    embed = discord.Embed(
        title="Who are we?",
        description="The [Pyth Alligators](https://magiceden.io/marketplace/pyth_alligators) (also known as DeleGators) are a collection of 100 generative NFTs launched on Solana through Burnt Finance’s Ignition Launchpad. They are a part of the Serum NFT Ecosystem and Pyth Network’s very own NFT collection.",
        color=discord.Color.from_str("#238a52")

    )
    embed.set_thumbnail(url="https://i.imgur.com/VIQloL2.png")
    embed.set_author(name="Pyth Alligators", url="https://magiceden.io/marketplace/pyth_alligators", icon_url=f"https://img-cdn.magiceden.dev/rs:fit:640:640:0:0/plain/{floor_img}")
    # You can add more fields to the embed if needed
    embed.add_field(name="Floor", value=f"[{floor} SOL](https://magiceden.io/item-details/{floor_listing}?name=Pyth-Alligators)")
    embed.add_field(name="Total Supply", value="99")
    embed.add_field(name="Unique Holders", value=num_of_unique_holders)
    embed.add_field(name="Gators Listed", value=listed_count)
    embed.add_field(name="All Vol", value=all_volume)
    embed.add_field(name="Last Sale", value=f"[{last_sale}d ago](https://solana.fm/tx/{signature})")

    # Send the embed message
    await ctx.send(embed=embed)


# @bot.command()
# async def check_permission(ctx):
#     # Get the channel where the command was invoked
#     channel = ctx.channel
#
#     # Get the bot member object
#     bot_member = ctx.guild.get_member(bot.user.id)
#
#     if bot_member:
#         # Check if the bot has the 'send_messages' permission in the channel
#         permissions = channel.permissions_for(bot_member)
#
#         if permissions.embed_links:
#             await ctx.send('I have the permission to send embeds in this channel.')
#         else:
#             await ctx.send('I do not have the permission to send embeds in this channel.')
#     else:
#         await ctx.send('I couldn\'t find myself in this server.')

# async def new_listing():
#     old_listed_count = 0
#     while True:
#         floor, listed_count = await floor_price()
#         if listed_count > old_listed_count:
#             message = f"New Gator has been listed! <:hmm:877428198625914910> https://magiceden.io/marketplace/pyth_alligators \nTotal listed: {listed_count} <:pepelove:877222447273873438>"
#             channel_id = 1100116676432904364
#             channel = client.get_channel(channel_id)
#             await channel.send(message)
#         await asyncio.sleep(60)
#         old_listed_count = listed_count


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    bot.loop.create_task(update_activity())
    # client.loop.create_task(new_listing())

bot.run(TOKEN)
