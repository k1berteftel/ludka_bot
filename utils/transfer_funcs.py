import asyncio
import aiohttp

from config_data.config import Config, load_config

config: Config = load_config()


BASE_URL = 'https://robynhood.parssms.info/'


async def transfer_stars(username: str, amount: int) -> bool:
    url = BASE_URL + 'api/purchase'
    headers = {
        'X-API-Key': config.fragment.api_key
    }
    data = {
        "product_type": "stars",
        "recipient": username,
        "quantity":  str(amount),
        #"idempotency_key": config.fragment.api_key
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers) as response:
            if response.status not in [200, 201]:
                print(await response. json())
                return False
            data = await response.json()
            print(data)
    return True


#asyncio.run(transfer_stars('SII_AST', 50))