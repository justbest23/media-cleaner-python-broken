from plex_api import get  # Assuming you have a plex_api.py file
from shared import MediaType  # Assuming you have a shared.py file with MediaType enum

class PlexData:
    def __init__(self, title):
        self.title = title

    @classmethod
    async def get_data(cls, rating_key, media_type):
        path = f"/library/metadata/{rating_key}"
        if media_type == MediaType.Movie:
            raw_plex_data = await get(path)
            return cls(raw_plex_data.find(".//Video").attrib['title'])
        elif media_type == MediaType.Tv:
            raw_plex_data = await get(path)
            return cls(raw_plex_data.find(".//Directory").attrib['title'])
