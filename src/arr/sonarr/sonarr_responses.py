from enum import Enum
from typing import Optional, List

class SeriesStatus(Enum):
    CONTINUING = "Continuing"
    ENDED = "Ended"
    UPCOMING = "Upcoming"
    DELETED = "Deleted"

class SeriesStatisticsResource:
    def __init__(self, season_count: int, episode_file_count: int, episode_count: int, size_on_disk: int, percent_of_episodes: float):
        self.season_count = season_count
        self.episode_file_count = episode_file_count
        self.episode_count = episode_count
        self.size_on_disk = size_on_disk
        self.percent_of_episodes = percent_of_episodes

class SeasonStatisticsResource:
    def __init__(self, episode_count: int):
        self.episode_count = episode_count

class SeasonResource:
    def __init__(self, season_number: int, statistics: SeasonStatisticsResource):
        self.season_number = season_number
        self.statistics = statistics

class SeriesResource:
    def __init__(self, id: int, title: Optional[str], status: SeriesStatus, previous_airing: Optional[str], next_airing: Optional[str], statistics: SeriesStatisticsResource, seasons: List[SeasonResource]):
        self.id = id
        self.title = title
        self.status = SeriesStatus(status)
        self.previous_airing = previous_airing
        self.next_airing = next_airing
        self.statistics = statistics
        self.seasons = seasons

    @classmethod
    def from_json(cls, json_data):
        return cls(
            id=json_data.get('id'),
            title=json_data.get('title'),
            status=SeriesStatus(json_data.get('status')),
            previous_airing=json_data.get('previousAiring'),
            next_airing=json_data.get('nextAiring'),
            statistics=SeriesStatisticsResource(**json_data.get('statistics', {})),
            seasons=[SeasonResource(**season) for season in json_data.get('seasons', [])]
        )
