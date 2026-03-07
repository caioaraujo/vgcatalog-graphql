from sqlalchemy.orm import Session

from app.domain.models import Game


class GameRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_name_and_platform(self, name: str, platform: str):
        return self.db.query(Game).filter_by(name=name, platform=platform).first()

    def create_or_update(self, game: Game):
        self.db.add(game)
        self.db.commit()
        self.db.refresh(game)
        return game

    def get_by_id(self, game_id: int):
        return self.db.get(Game, game_id)

    def get_by_filter(
        self,
        name=None,
        platform=None,
        genre=None,
        released_year=None,
        allow_multiplayer=None,
    ):
        query = self.db.query(Game)
        if name:
            query = query.filter(Game.name == name)
        if platform:
            query = query.filter(Game.platform == platform)
        if genre:
            query = query.filter(Game.genre == genre)
        if released_year is not None:
            query = query.filter(Game.released_year == released_year)
        if allow_multiplayer is not None:
            query = query.filter(Game.allow_multiplayer == allow_multiplayer)
        return query.all()
