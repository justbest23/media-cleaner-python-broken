from config import Config  # Assuming you have a Config class in a config.py file
import aiohttp
from urllib.parse import urlencode

async def get(path, params=None):
    async with aiohttp.ClientSession() as session:
        config = Config.global_instance().overseerr
        params_str = urlencode(params) if params else ""
        url = f"{config['url']}/api/v1{path}?take=100&{params_str}"
        headers = {'X-API-Key': config['api_key']}
        
        async with session.get(url, headers=headers) as response:
            if response.status not in range(200, 300):
                raise Exception(f"Failed to fetch data from Overseerr. Status code: {response.status}")
            return await response.json()

async def delete(path):
    async with aiohttp.ClientSession() as session:
        config = Config.global_instance().overseerr
        url = f"{config['url']}/api/v1{path}"
        headers = {'X-API-Key': config['api_key']}
        
        async with session.delete(url, headers=headers) as response:
            if response.status not in range(200, 300):
                raise Exception(f"Failed to delete data in Overseerr. Status code: {response.status}")
            return True
