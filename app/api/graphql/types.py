import strawberry


@strawberry.type
class GameType:
    id: int
    name: str
    genre: str | None
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
    name: str | None
    genre: str | None
    platform: str | None
    released_year: int | None
    allow_multiplayer: bool | None
