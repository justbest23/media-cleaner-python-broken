from datetime import datetime
from typing import List, Optional, Union
from collections import defaultdict
from tautulli_api import get_obj  # Assuming you have an api.py file in the tautulli folder
from shared import MediaType  # Assuming you have a shared.py file
from tautulli_responses import HistoryItem, HistoryMovieItem  # Assuming you have a responses.py file in the tautulli folder

class WatchHistory:
    def __init__(self, watches: Union[List['UserMovieWatch'], List['UserEpisodeWatch']]):
        self.watches = watches

    @classmethod
    def from_user_watches(cls, user_watches: dict, media_type: MediaType, rating_key: str):
        if media_type == MediaType.MOVIE:
            return cls.create_movie_history(user_watches, rating_key)
        elif media_type == MediaType.TV:
            return cls.create_tv_history(user_watches, rating_key)

    @classmethod
    def create_movie_history(cls, user_watches: dict, rating_key: str):
        watches = [
            UserMovieWatch(
                display_name=user,
                last_watched=datetime.utcfromtimestamp(movie_watch.date),
                progress=movie_watch.percent_complete
            )
            for user, movie_watch in user_watches.items()
        ]
        return cls(watches)

    @classmethod
    def create_tv_history(cls, user_watches: dict, rating_key: str):
        watches = [
            UserEpisodeWatch(
                display_name=user,
                last_watched=datetime.utcfromtimestamp(tv_watch.date),
                progress=tv_watch.percent_complete,
                season=tv_watch.parent_media_index,
                episode=tv_watch.media_index
            )
            for user, tv_watch in user_watches.items()
        ]
        return cls(watches)

    def __str__(self):
        return "\n".join(str(watch) for watch in self.watches)

class UserEpisodeWatch:
    def __init__(self, display_name: str, last_watched: datetime, progress: int, season: int, episode: int):
        self.display_name = display_name
        self.last_watched = last_watched
        self.progress = progress
        self.season = season
        self.episode = episode

    def __str__(self):
        return f"Last watch by {self.display_name} was at {self.last_watched.strftime('%d-%m-%Y')}. Season {self.season} Episode {self.episode}, with {self.progress}% complete."

class UserMovieWatch:
    def __init__(self, display_name: str, last_watched: datetime, progress: int):
        self.display_name = display_name
        self.last_watched = last_watched
        self.progress = progress

    def __str__(self):
        return f"Last watch by {self.display_name} at {self.last_watched.strftime('%d-%m-%Y')}, with {self.progress}% progress."

async def get_item_watches(rating_key: str, media_type: MediaType) -> WatchHistory:
    params = [("rating_key", rating_key)]
    history_data = await get_obj("get_history", params)
    user_watches = defaultdict(list)

    for item in history_data:
        if media_type == MediaType.MOVIE:
            user_watches[item.user].append(HistoryMovieItem.from_dict(item))
        elif media_type == MediaType.TV:
            user_watches[item.user].append(HistoryItem.from_dict(item))

    return WatchHistory.from_user_watches(user_watches, media_type, rating_key)

async def get_item_history(rating_key: str, media_type: MediaType) -> WatchHistory:
    params = [("rating_key", rating_key)]
    history_data = await get_obj("get_history", params)
    user_watches = defaultdict(list)

    for item in history_data:
        if media_type == MediaType.MOVIE:
            user_watches[item.user].append(HistoryMovieItem.from_dict(item))
        elif media_type == MediaType.TV:
            user_watches[item.user].append(HistoryItem.from_dict(item))

    return WatchHistory.from_user_watches(user_watches, media_type, rating_key)

async def get_full_history(media_type: MediaType) -> List[WatchHistory]:
    params = [("media_type", media_type.value)]
    history_data = await get_obj("get_full_history", params)
    full_history = []

    for rating_key, user_watches in history_data.items():
        watch_history = WatchHistory.from_user_watches(user_watches, media_type, rating_key)
        full_history.append(watch_history)

    return full_history


def movie_item_to_history_item(movie_item: dict) -> HistoryMovieItem:
    return HistoryMovieItem.from_dict(movie_item)

def unix_seconds_to_date(unix_seconds: int) -> datetime:
    return datetime.utcfromtimestamp(unix_seconds)