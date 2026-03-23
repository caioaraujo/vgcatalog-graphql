from enum import Enum
from typing import Optional, List

import strawberry


@strawberry.enum
class SortDirection(Enum):
    ASC = "asc"
    DESC = "desc"


@strawberry.input
class StringFilterInput:
    eq: Optional[str] = None
    contains: Optional[str] = None
    in_list: Optional[List[str]] = None


@strawberry.input
class IntFilter:
    eq: Optional[int] = None
    gt: Optional[int] = None
    lt: Optional[int] = None


@strawberry.input
class BooleanFilter:
    eq: Optional[bool] = None


@strawberry.input
class PaginationInput:
    limit: Optional[int] = 10
    offset: Optional[int] = 0


@strawberry.input
class SortInput:
    field: str
    direction: SortDirection = SortDirection.ASC


@strawberry.type
class GameType:
    id: int
    name: str
    genre: Optional[str] = None
    platform: str
    released_year: int
    allow_multiplayer: bool


@strawberry.input
class GameInput:
    name: str
    genre: str
    platform: str
    released_year: int
    allow_multiplayer: bool


@strawberry.input
class GameFilterInput:
    name: Optional[StringFilterInput] = None
    genre: Optional[StringFilterInput] = None
    platform: Optional[StringFilterInput] = None
    released_year: Optional[IntFilter] = None
    allow_multiplayer: Optional[BooleanFilter] = None
    pagination: Optional[PaginationInput] = None
    sort: Optional[SortInput] = None
