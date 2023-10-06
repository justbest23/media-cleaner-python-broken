from datetime import datetime
from overseerr_api import get, delete  # Assuming you have an overseerr_api.py file
from config import Config  # Assuming you have a Config class in a config.py file

class MediaRequest:
    def __init__(self, id, media_id, rating_key, manager_id, manager_4k_id, created_at, updated_at, requested_by, media_status, media_type):
        self.id = id
        self.media_id = media_id
        self.rating_key = rating_key
        self.manager_id = manager_id
        self.manager_4k_id = manager_4k_id
        self.created_at = created_at
        self.updated_at = updated_at
        self.requested_by = requested_by
        self.media_status = media_status
        self.media_type = media_type

    async def remove_request(self):
        path = f"/media/{self.media_id}"
        await delete(path)

    @classmethod
    async def get_all(cls):
        response_data = await get("/request", None)
        requests = [cls.from_response(r) for r in response_data['results']]
        return requests

    @classmethod
    def from_response(cls, response):
        # Your conversion logic here
        pass

class ServerItem:
    def __init__(self, id, rating_key, manager_id, manager_id_4k, created_at, updated_at, media_status, media_type):
        self.id = id
        self.rating_key = rating_key
        self.manager_id = manager_id
        self.manager_id_4k = manager_id_4k
        self.created_at = created_at
        self.updated_at = updated_at
        self.media_status = media_status
        self.media_type = media_type

    @classmethod
    async def get_all(cls):
        response_data = await get("/media", {"filter": "available"})
        requests = [cls.from_response(r) for r in response_data['results']]
        return requests

    @classmethod
    def from_response(cls, response):
        # Your conversion logic here
        pass
