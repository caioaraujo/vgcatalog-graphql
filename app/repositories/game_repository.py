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
