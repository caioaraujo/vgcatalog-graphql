import strawberry

@strawberry.type
class GameType:
    id: int
    name: str
    genre: str | None
    platform: str
    released_year: int
    allow_multiplayer: bool

