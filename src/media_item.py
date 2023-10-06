from typing import Optional, Union
from shared import MediaType, MediaStatus, MediaRequest, WatchHistory, ArrData
from colorama import Fore
import asyncio
from config import Config
import arr.arr_mod
import errors

class MediaItem:
    def __init__(self, title: Optional[str] = None, rating_key: Optional[str] = None,
                 manager_id: Optional[int] = None, manager_4k_id: Optional[int] = None,
                 media_type: MediaType = None, media_status: MediaStatus = None,
                 request: Optional[MediaRequest] = None):
        self.title = title
        self.rating_key = rating_key
        self.manager_id = manager_id
        self.manager_4k_id = manager_4k_id
        self.media_type = media_type
        self.media_status = media_status
        self.request = request

    @classmethod
    def from_request(cls, request: MediaRequest):
        return cls(
            rating_key=request.rating_key,
            manager_id=request.manager_id,
            manager_4k_id=request.manager_4k_id,
            media_type=request.media_type,
            media_status=request.media_status,
            request=request
        )

    @classmethod
    def from_server_item(cls, item: ServerItem):
        return cls(
            rating_key=item.rating_key,
            manager_id=item.manager_id,
            manager_4k_id=item.manager_id_4k,
            media_type=item.media_type,
            media_status=item.media_status
        )

    async def into_complete_media(self):
        metadata = self.retrieve_metadata()
        history = self.retrieve_history()
        data = self.retrieve_arr_data()

        details, history, (arr_data, arr_4k_data) = await asyncio.gather(metadata, history, data)
        return CompleteMediaItem(
            title=details.title,
            media_type=self.media_type,
            request=self.request,
            history=history,
            arr_data=arr_data,
            arr_4k_data=arr_4k_data
        )

    def is_available(self):
        return self.media_status in [MediaStatus.AVAILABLE, MediaStatus.PARTIALLY_AVAILABLE]

    def has_manager_active(self):
        return arr.movie_manager_active() if self.media_type == MediaType.MOVIE else arr.tv_manager_active()

    def user_ignored(self):
        if self.request is None:
            return False
        ignored_users = Config.global_config().ignored_users
        return self.request.requested_by in ignored_users if ignored_users else False

    async def retrieve_history(self):
        if self.rating_key is None:
            raise errors.NoRatingKeyException()
        return await tautulli.get_item_watches(self.rating_key, self.media_type)

    async def retrieve_metadata(self):
        if self.rating_key is None:
            raise errors.NoRatingKeyException("No rating key was found for the request. Unable to gather metadata.")
        return await PlexData.get_data(self.rating_key, self.media_type)

    async def retrieve_arr_data(self):
        if self.manager_id is None and self.manager_4k_id is None:
            raise errors.NoArrIdException()
        data_standard = ArrData.get_data(self.media_type, self.manager_id) if self.manager_id else None
        data_4k = ArrData.get_4k_data(self.media_type, self.manager_4k_id) if self.manager_4k_id else None
        return await asyncio.gather(data_standard, data_4k)

class CompleteMediaItem:
    def __init__(self, title: str, media_type: MediaType, request: Optional[MediaRequest],
                 history: WatchHistory, arr_data: Optional[ArrData], arr_4k_data: Optional[ArrData]):
        self.title = title
        self.media_type = media_type
        self.request = request
        self.history = history
        self.arr_data = arr_data
        self.arr_4k_data = arr_4k_data

    async def remove_from_server(self):
        if self.request:
            await self.request.remove_request()
        if self.arr_data:
            await self.arr_data.remove_data()
        if self.arr_4k_data:
            await self.arr_4k_data.remove_data()

    def get_disk_size(self):
        if self.arr_data and self.arr_4k_data:
            return self.arr_data.get_disk_size() + self.arr_4k_data.get_disk_size()
        elif self.arr_data:
            return self.arr_data.get_disk_size()
        elif self.arr_4k_data:
            return self.arr_4k_data.get_disk_size()
        else:
            raise errors.NonExistentObjectException()

    def __str__(self):
        return f"CompleteMediaItem(title={self.title}, media_type={self.media_type}, request={self.request}, history={self.history}, arr_data={self.arr_data}, arr_4k_data={self.arr_4k_data})"


# Implement other methods here
