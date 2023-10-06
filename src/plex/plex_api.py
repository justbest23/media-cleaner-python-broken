from config import Config  # Assuming you have a Config class in a config.py file
import aiohttp
from xml.etree import ElementTree as ET

async def get(path, params=None):
    async with aiohttp.ClientSession() as session:
        config = Config.global_instance().plex
        url = f"{config['url']}{path}?X-Plex-Token={config['token']}"
        
        async with session.get(url) as response:
            if response.status not in range(200, 300):
                raise Exception(f"Failed to fetch data from Plex. Status code: {response.status}")
            
            response_text = await response.text()
            parsed_response = ET.fromstring(response_text)
            return parsed_response
