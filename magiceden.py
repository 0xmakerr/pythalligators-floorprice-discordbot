import aiohttp
import time
import asyncio

url = "https://api-mainnet.magiceden.dev/v2/collections/pyth_alligators/stats"  # Include the scheme here
payload = {}
headers = {}

async def floor_price():
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, data=payload) as response:
            json_response = await response.json()
            floor = int(json_response["floorPrice"] / 1e9)
            return floor