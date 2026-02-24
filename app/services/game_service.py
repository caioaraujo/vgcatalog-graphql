from sqlalchemy.orm import Session

from app.models.game import Game
from app.schemas.game import GameCreate


class GameService:

    def create_game(self, db: Session, game: GameCreate):
        db_game = Game(
            name=game.name,
            released_year=game.released_year,
            platform=game.platform,
            genre=game.genre,
            allow_multiplayer=game.allow_multiplayer,
        )
        db.add(db_game)
        db.commit()
        db.refresh(db_game)
        return db_game
