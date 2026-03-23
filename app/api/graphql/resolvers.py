from typing import List, Optional
import strawberry
from graphql import GraphQLError
from strawberry.types import Info

from app.domain.exceptions import GameNotFoundException
from app.schemas.game import GameCreate, GameList
from app.api.graphql.types import GameType, GameFilterInput, GameInput


@strawberry.type
class Query:

    @strawberry.field
    def game(self, info: Info, game_id: int) -> Optional[GameType]:
        service = info.context["game_service"]
        try:
            game = service.fetch_game(game_id)
        except GameNotFoundException as e:
            raise GraphQLError(str(e))
        if not game:
            return None
        return GameType(
            id=game.id,
            name=game.name,
            genre=game.genre,
            platform=game.platform,
            released_year=game.released_year,
            allow_multiplayer=game.allow_multiplayer,
        )

    @strawberry.field
    def games(self, info: Info, data: GameFilterInput) -> List[GameType]:
        game_data = GameList(
            name=data.name,
            genre=data.genre,
            released_year=data.released_year,
            platform=data.platform,
            allow_multiplayer=data.allow_multiplayer,
        )
        service = info.context["game_service"]
        games = service.list_games(game_data)
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
        game_data = GameCreate(
            name=data.name,
            genre=data.genre,
            released_year=data.released_year,
            platform=data.platform,
            allow_multiplayer=data.allow_multiplayer,
        )
        service = info.context["game_service"]
        created = service.create_game(game_data)
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
        game_data = GameCreate(
            name=data.name,
            genre=data.genre,
            released_year=data.released_year,
            platform=data.platform,
            allow_multiplayer=data.allow_multiplayer,
        )
        service = info.context["game_service"]
        updated = service.update_game(game_id, game_data)
        return GameType(
            id=updated.id,
            name=updated.name,
            genre=updated.genre,
            released_year=updated.released_year,
            platform=updated.platform,
            allow_multiplayer=updated.allow_multiplayer,
        )
