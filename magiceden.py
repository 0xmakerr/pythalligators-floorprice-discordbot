import aiohttp
import time
import asyncio
import datetime

stats_url = "https://api-mainnet.magiceden.dev/v2/collections/pyth_alligators/stats"  # Include the scheme here
holder_stats_url = "https://api-mainnet.magiceden.dev/v2/collections/pyth_alligators/holder_stats"
listings_url = "https://api-mainnet.magiceden.dev/v2/collections/pyth_alligators/listings"
activities_url = "https://api-mainnet.magiceden.dev/v2/collections/pyth_alligators/activities"
payload = {}
headers = {}


def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])


async def floor_price():
    async with aiohttp.ClientSession() as session:
        async with session.get(stats_url, headers=headers, data=payload) as response:
            json_response = await response.json()
            floor = int(json_response["floorPrice"] / 1e9)
            listed_count = json_response["listedCount"]
            all_volume = human_format(int(json_response["volumeAll"] / 1e9))
            return floor, listed_count, all_volume


async def unique_holders():
    async with aiohttp.ClientSession() as session:
        async with session.get(holder_stats_url, headers=headers, data=payload) as response:
            json_response = await response.json()
            num_of_unique_holders = json_response["uniqueHolders"]
            return num_of_unique_holders


async def listings():
    async with aiohttp.ClientSession() as session:
        async with session.get(listings_url, headers=headers, data=payload) as response:
            json_response = await response.json()
            floor_listing = json_response[0]["tokenMint"]
            floor_img = json_response[0]["extra"]["img"]
            return floor_listing, floor_img


async def activities():
    async with aiohttp.ClientSession() as session:
        async with session.get(activities_url, headers=headers, data=payload) as response:
            json_response = await response.json()
            buyers = [item for item in json_response if item["type"] == "buyNow"]
            signature = buyers[0]["signature"]
            last_sale_unix = buyers[0]["blockTime"]
            last_sale_time = datetime.datetime.fromtimestamp(last_sale_unix)
            time_now = datetime.datetime.now()
            sale_days_ago = time_now - last_sale_time
            last_sale_days = sale_days_ago.days
            return last_sale_days, signature
