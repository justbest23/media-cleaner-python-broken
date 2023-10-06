from enum import Enum
from typing import Optional

class MovieStatus(Enum):
    TO_BE_ANNOUNCED = "tba"
    ANNOUNCED = "announced"
    IN_CINEMAS = "inCinemas"
    RELEASED = "released"
    DELETED = "deleted"

class MovieResource:
    def __init__(self, id: int, title: Optional[str], status: MovieStatus, size_on_disk: int, digital_release: Optional[str], physical_release: Optional[str]):
        self.id = id
        self.title = title
        self.status = MovieStatus(status)
        self.size_on_disk = size_on_disk
        self.digital_release = digital_release
        self.physical_release = physical_release

    @classmethod
    def from_json(cls, json_data):
        return cls(
            id=json_data.get('id'),
            title=json_data.get('title'),
            status=MovieStatus(json_data.get('status')),
            size_on_disk=json_data.get('sizeOnDisk'),
            digital_release=json_data.get('digitalRelease'),
            physical_release=json_data.get('physicalRelease')
        )
