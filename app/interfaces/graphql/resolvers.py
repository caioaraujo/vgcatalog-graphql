from typing import List, Optional
import strawberry
from strawberry.types import Info

from app.interfaces.graphql.mappers import to_game_type, to_game_list
from app.schemas.game import GameCreate, GameList
from app.interfaces.graphql.types import GameType, GameFilterInput, GameInput


@strawberry.type
class Query:

    @strawberry.field
    def game(self, info: Info, game_id: int) -> Optional[GameType]:
        service = info.context["game_service"]
        game = service.fetch_game(game_id)
        return to_game_type(game)

    @strawberry.field
    def games(self, info: Info, data: GameFilterInput) -> List[GameType]:
        game_data = to_game_list(data)
        service = info.context["game_service"]
        games = service.list_games(game_data)
        return [to_game_type(g) for g in games]


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
        return to_game_type(created)

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
        return to_game_type(updated)
