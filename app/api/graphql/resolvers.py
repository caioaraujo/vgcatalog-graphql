from typing import List, Optional
import strawberry
from graphql import GraphQLError
from strawberry.types import Info
from sqlalchemy.orm import Session

from app.domain.exceptions import GameAlreadyExistsException
from app.repositories.game_repository import GameRepository
from app.schemas.game import GameCreate, GameList
from app.services.game_service import GameService
from app.api.graphql.types import GameType, GameFilterInput, GameInput


@strawberry.type
class Query:

    @strawberry.field
    def game(self, info: Info, game_id: int) -> Optional[GameType]:
        db: Session = info.context["db"]
        repository = GameRepository(db)
        try:
            game = GameService(repository).fetch_game(game_id)
        except GameAlreadyExistsException as e:
            raise GraphQLError(str(e))
        if not game:
            return None
        return GameType(id=game.id, name=game.name, genre=game.genre)

    @strawberry.field
    def games(self, info: Info, data: GameFilterInput) -> List[GameType]:
        db: Session = info.context["db"]
        repository = GameRepository(db)
        game_data = GameList(
            name=data.name,
            genre=data.genre,
            released_year=data.released_year,
            platform=data.platform,
            allow_multiplayer=data.allow_multiplayer,
        )
        games = GameService(repository).list_games(game_data)
        return [
            GameType(
                id=g.id,
                name=g.name,
                genre=g.genre,
                platform=g.platform,
                released_year=g.released_year,
                allow_multiplayer=g.allow_multiplayer,
            )
            for g in games
        ]


@strawberry.type
class Mutation:

    @strawberry.mutation
    def create_game(self, info: Info, data: GameInput) -> GameType:
        db: Session = info.context["db"]
        repository = GameRepository(db)
        game_data = GameCreate(
            name=data.name,
            genre=data.genre,
            released_year=data.released_year,
            platform=data.platform,
            allow_multiplayer=data.allow_multiplayer,
        )
        created = GameService(repository).create_game(game_data)
        return GameType(
            id=created.id,
            name=created.name,
            genre=created.genre,
            released_year=created.released_year,
            platform=created.platform,
            allow_multiplayer=created.allow_multiplayer,
        )

    @strawberry.mutation
    def update_game(self, info: Info, game_id: int, data: GameInput) -> GameType:
        db: Session = info.context["db"]
        repository = GameRepository(db)
        game_data = GameCreate(
            name=data.name,
            genre=data.genre,
            released_year=data.released_year,
            platform=data.platform,
            allow_multiplayer=data.allow_multiplayer,
        )
        updated = GameService(repository).update_game(game_id, game_data)
        return GameType(
            id=updated.id,
            name=updated.name,
            genre=updated.genre,
            released_year=updated.released_year,
            platform=updated.platform,
            allow_multiplayer=updated.allow_multiplayer,
        )
