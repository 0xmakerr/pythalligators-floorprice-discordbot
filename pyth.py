import asyncio
import pythclient.exceptions
from pythclient.pythaccounts import PythPriceAccount, PythPriceStatus
from pythclient.solana import SolanaClient, SolanaPublicKey, PYTHNET_HTTP_ENDPOINT, PYTHNET_WS_ENDPOINT

async def get_price():
    # pythnet SOL/USD price account key (available on pyth.network website)
    account_key = SolanaPublicKey("H6ARHf6YXhGYeQfUzQNGk6rDNnLBQKrenN712K4AQJEG")
    solana_client = SolanaClient(endpoint=PYTHNET_HTTP_ENDPOINT, ws_endpoint=PYTHNET_WS_ENDPOINT)
    price: PythPriceAccount = PythPriceAccount(account_key, solana_client)

    while True:
        try:
            await price.update()
            price_status = price.aggregate_price_status
            if price_status == PythPriceStatus.TRADING:
                solprice = price.aggregate_price
                return solprice
            else:
                print("Price is not valid now. Status is", price_status)
        except pythclient.exceptions.SolanaException:
            print("pythclient.exceptions.SolanaException. Waiting 60 seconds and trying again.")
            await asyncio.sleep(60)
        finally:
            await solana_client.close()
