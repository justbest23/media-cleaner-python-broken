class NoRatingKeyException(Exception):
    def __init__(self, message="No rating key was found for the request. Unable to gather watch history."):
        super().__init__(message)

class NoArrIdException(Exception):
    def __init__(self, message="No *arr ID was found for the request. Unable to gather file data."):
        super().__init__(message)

class IncompleteMediaException(Exception):
    def __init__(self, message="Incomplete media item. Missing essential data."):
        super().__init__(message)

class NonExistentObjectException(Exception):
    def __init__(self, message="Tried to get the size of a non-existent object."):
        super().__init__(message)

class RequestRemovalException(Exception):
    def __init__(self, message="Error while removing the request."):
        super().__init__(message)

class DataRemovalException(Exception):
    def __init__(self, message="Error while removing data."):
        super().__init__(message)