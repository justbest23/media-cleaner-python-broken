from typing import List, Optional, TypeVar, Union
from enum import Enum
from pydantic import BaseModel

T = TypeVar("T")

class ResultType(str, Enum):
    SUCCESS = "Success"
    ERROR = "Error"

class ResponseInternalArr(BaseModel):
    message: Optional[str]
    result: ResultType
    data: List[T]

class ResponseArr(BaseModel):
    response: ResponseInternalArr[T]

class ResponseInternalObj(BaseModel):
    message: Optional[str]
    result: ResultType
    data: T

class ResponseObj(BaseModel):
    response: ResponseInternalObj[T]

class HistoryItem(BaseModel):
    user: str
    date: int
    duration: int
    percent_complete: int
    media_index: Optional[int]
    parent_media_index: Optional[int]

class HistoryMovieItem(BaseModel):
    date: int
    duration: int
    percent_complete: int
    user: str

class History(BaseModel):
    draw: int
    records_total: int
    records_filtered: int
    data: List[T]
