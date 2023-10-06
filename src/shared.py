from enum import Enum, auto
from typing import Union

class MediaType(Enum):
    Movie = auto()
    Tv = auto()

class Order(Enum):
    Desc = auto()
    Asc = auto()

class SortingValue(Enum):
    Name = auto()
    Size = auto()
    Type = auto()

class SortingOption:
    def __init__(self, sorting_value: SortingValue, sorting_direction: Order):
        self.sorting_value = sorting_value
        self.sorting_direction = sorting_direction

    @classmethod
    def from_str(cls, s: str):
        if s == "nd":
            return cls(SortingValue.Name, Order.Desc)
        elif s == "n":
            return cls(SortingValue.Name, Order.Asc)
        elif s == "sa":
            return cls(SortingValue.Size, Order.Asc)
        elif s == "s":
            return cls(SortingValue.Size, Order.Desc)
        elif s == "t":
            return cls(SortingValue.Type, Order.Desc)
        else:
            raise ValueError("Not a valid Sorting Option")
