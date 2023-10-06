from enum import Enum

class RequestResponse:
    def __init__(self, page_info, results):
        self.page_info = page_info
        self.results = results

class PageInfo:
    def __init__(self, page, pages, results, page_size):
        self.page = page
        self.pages = pages
        self.results = results
        self.page_size = page_size

class UserResponse:
    def __init__(self, id, email, display_name):
        self.id = id
        self.email = email
        self.display_name = display_name

class MediaResponse:
    def __init__(self, id, external_service_id, external_service_id_4k, rating_key, status, media_type, created_at, updated_at):
        self.id = id
        self.external_service_id = external_service_id
        self.external_service_id_4k = external_service_id_4k
        self.rating_key = rating_key
        self.status = status
        self.media_type = media_type
        self.created_at = created_at
        self.updated_at = updated_at

class MediaStatus(Enum):
    UNKNOWN = 1
    PENDING = 2
    PROCESSING = 3
    PARTIALLY_AVAILABLE = 4
    AVAILABLE = 5

class MediaRequestResponse:
    def __init__(self, id, media, created_at, updated_at, requested_by):
        self.id = id
        self.media = media
        self.created_at = created_at
        self.updated_at = updated_at
        self.requested_by = requested_by
