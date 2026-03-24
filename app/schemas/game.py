from pydantic import BaseModel
from typing import Optional, List


class GameCreate(BaseModel):
    name: str
    released_year: int
    platform: str
    genre: str
    allow_multiplayer: bool


class Game(BaseModel):
    id: int
    name: str
    released_year: int
    platform: str
    genre: str
    allow_multiplayer: bool


class StringFilter(BaseModel):
    eq: Optional[str] = None
    contains: Optional[str] = None
    in_list: Optional[List[str]] = None


class IntFilter(BaseModel):
    eq: Optional[int] = None
    gt: Optional[int] = None
    lt: Optional[int] = None


class BooleanFilter(BaseModel):
    eq: Optional[bool] = None


class SortInput(BaseModel):
    field: str
    direction: str


class PaginationInput(BaseModel):
    limit: int
    offset: int


class GameList(BaseModel):
    name: Optional[StringFilter] = None
    released_year: Optional[IntFilter] = None
    platform: Optional[StringFilter] = None
    genre: Optional[StringFilter] = None
    allow_multiplayer: Optional[BooleanFilter] = None
    pagination: Optional[PaginationInput] = None
    sort: Optional[SortInput] = None
