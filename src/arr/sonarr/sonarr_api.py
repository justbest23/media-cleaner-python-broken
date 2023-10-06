from config import Config  # Assuming you have a Config class in a config.py file
import aiohttp
from urllib.parse import urlencode

async def get(path, params=None, is_4k=False):
    async with aiohttp.ClientSession() as session:
        config = Config.global_instance().sonarr_4k if is_4k else Config.global_instance().sonarr
        params_str = urlencode(params) if params else ""
        url = f"{config['url']}/api/v3{path}?{params_str}"
        headers = {'X-Api-Key': config['api_key']}
        
        async with session.get(url, headers=headers) as response:
            if response.status not in range(200, 300):
                raise Exception(f"Failed to fetch data from Sonarr. Status code: {response.status}")
            return await response.json()

async def delete(path, params=None):
    async with aiohttp.ClientSession() as session:
        config = Config.global_instance().sonarr
        params_str = urlencode(params) if params else ""
        url = f"{config['url']}/api/v3{path}?{params_str}"
        headers = {'X-Api-Key': config['api_key']}
        
        async with session.delete(url, headers=headers) as response:
            if response.status not in range(200, 300):
                raise Exception(f"Failed to delete data in Sonarr. Status code: {response.status}")
            return True
