import datetime

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.domain.repositories.game_repository import GameRepository
from app.infra.orm.models import Game
from app.schemas.game import GameList


class GameRepositoryImpl(GameRepository):
    def __init__(self, db: Session, clock: Clock):
        self.db = db
        self.clock = clock

    def get_by_name_and_platform(self, name: str, platform: str):
        return self.db.query(Game).filter_by(name=name, platform=platform).first()

    def create_or_update(self, game: Game):
        if not game.created_at:
            game.created_at = self.clock.now()
        self.db.add(game)
        self.db.commit()
        self.db.refresh(game)
        return game

    def get_by_id(self, game_id: int):
        return self.db.get(Game, game_id)

    def get_by_filter(self, filters: GameList):
        query = self.db.query(Game)
        query = self._filter_str_field(filters.name, Game.name, query)
        query = self._filter_str_field(filters.platform, Game.platform, query)
        query = self._filter_str_field(filters.genre, Game.genre, query)
        query = self._filter_int_field(filters.released_year, Game.released_year, query)
        if filters.allow_multiplayer and filters.allow_multiplayer.eq is not None:
            query = query.filter(Game.allow_multiplayer == filters.allow_multiplayer.eq)
        query = self._paginate(query, filters.pagination)
        query = self._sort(query, filters.sort)
        return query.all()

    def _filter_str_field(self, value, field, query):
        if not value:
            return query
        if value.eq is not None:
            return query.filter(field == value.eq)
        if value.contains is not None:
            return query.filter(field.ilike(f"%{value.contains}%"))
        if value.in_list:
            return query.filter(field.in_(value.in_list))
        return query

    def _filter_int_field(self, value, field, query):
        if not value:
            return query
        if value.eq is not None:
            return query.filter(field == value.eq)
        if value.gt is not None:
            return query.filter(field > value.gt)
        if value.lt is not None:
            return query.filter(field < value.lt)
        return query

    def _paginate(self, query, pagination):
        if pagination is not None:
            query = query.limit(pagination.limit).offset(pagination.offset)
        return query

    def _sort(self, query, sort):
        if sort is None:
            return query
        if sort.direction == "desc":
            return query.order_by(desc(sort.field))
        return query.order_by(sort.field)
