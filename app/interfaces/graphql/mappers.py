from app.interfaces.graphql.types import GameType, GameFilterInput
from app.schemas.game import (
    GameList,
    StringFilter,
    BooleanFilter,
    IntFilter,
    PaginationInput,
    SortInput,
)


def map_filter(filter_input, filter_class):
    if not filter_input:
        return None
    data = {k: v for k, v in vars(filter_input).items() if v is not None}
    return filter_class(**data)


def to_game_list(_input: GameFilterInput) -> GameList:
    return GameList(
        name=map_filter(_input.name, StringFilter),
        genre=map_filter(_input.genre, StringFilter),
        platform=map_filter(_input.platform, StringFilter),
        released_year=map_filter(_input.released_year, IntFilter),
        allow_multiplayer=map_filter(_input.allow_multiplayer, BooleanFilter),
        pagination=map_filter(_input.pagination, PaginationInput),
        sort=map_filter(_input.sort, SortInput),
    )


def to_game_type(game):
    return GameType(
        id=game.id,
        name=game.name,
        platform=game.platform,
        genre=game.genre,
        released_year=game.released_year,
        allow_multiplayer=game.allow_multiplayer,
    )
