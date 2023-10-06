from config import Config  # Assuming you have a Config class in a config.py file
from enum import Enum
from sonarr.sonarr_mod import get_sonarr_data, remove_sonarr_data_and_files  # Assuming you have a sonarr_mod.py file
from radarr.radarr_mod import get_radarr_data, remove_radarr_data_and_files  # Assuming you have a radarr_mod.py file

def movie_manager_active():
    return Config.global_instance().radarr is not None

def movie_4k_manager_active():
    return Config.global_instance().radarr_4k is not None

def tv_manager_active():
    return Config.global_instance().sonarr is not None

def tv_4k_manager_active():
    return Config.global_instance().sonarr_4k is not None

class MediaType(Enum):
    MOVIE = "Movie"
    TV = "Tv"

class ArrData:
    def __init__(self, media_type, id):
        self.media_type = media_type
        self.id = id

    @classmethod
    async def get_data(cls, media_type, id):
        if media_type == MediaType.MOVIE:
            return cls(MediaType.MOVIE, await get_radarr_data(id))
        elif media_type == MediaType.TV:
            return cls(MediaType.TV, await get_sonarr_data(id))

    @classmethod
    async def get_4k_data(cls, media_type, id):
        if media_type == MediaType.MOVIE:
            return cls(MediaType.MOVIE, await get_radarr_data(id, is_4k=True))
        elif media_type == MediaType.TV:
            return cls(MediaType.TV, await get_sonarr_data(id, is_4k=True))

    async def remove_data(self):
        if self.media_type == MediaType.MOVIE:
            await remove_radarr_data_and_files(self.id)
        elif self.media_type == MediaType.TV:
            await remove_sonarr_data_and_files(self.id)

    def get_disk_size(self):
        return self.id.size_on_disk
