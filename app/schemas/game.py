from pydantic import BaseModel


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
