from typing import Optional
import strawberry
from strawberry.types import Info
from sqlalchemy.orm import Session

from app.repositories.game_repository import GameRepository
from app.schemas.game import GameCreate
from app.services.game_service import GameService
from app.api.graphql.types import GameType


@strawberry.type
class Query:

    @strawberry.field
    def game(self, info: Info, game_id: int) -> Optional[GameType]:
        db: Session = info.context["db"]
        repository = GameRepository(db)
        game = GameService(repository).fetch_game(game_id)
        if not game:
            return None
        return GameType(id=game.id, name=game.name, genre=game.genre)


@strawberry.type
class Mutation:

    @strawberry.mutation
    def create_game(self, info: Info, name: str, genre: str, released_year: int, platform: str,
                    allow_multiplayer: bool) -> GameType:
        db: Session = info.context["db"]
        repository = GameRepository(db)
        game_create = GameCreate(name=name, genre=genre, released_year=released_year, platform=platform,
                                 allow_multiplayer=allow_multiplayer)
        created = GameService(repository).create_game(game_create)
        return GameType(id=created.id, name=created.name, genre=created.genre, released_year=released_year,
                        platform=platform, allow_multiplayer=allow_multiplayer)

    @strawberry.mutation
    def update_game(self, info: Info, game_id: int, name: str, genre: str, released_year: int, platform: str,
                    allow_multiplayer: bool) -> GameType:
        db: Session = info.context["db"]
        repository = GameRepository(db)
        game_update = GameCreate(name=name, genre=genre, released_year=released_year, platform=platform,
                                 allow_multiplayer=allow_multiplayer)
        updated = GameService(repository).update_game(game_id, game_update)
        return GameType(id=updated.id, name=updated.name, genre=updated.genre)
