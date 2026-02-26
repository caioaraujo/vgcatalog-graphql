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

    def update_game(self, db: Session, game_id: int, game: GameCreate):
        db_game = db.get(Game, game_id)
        if not db_game:
            return None
        db_game.name = game.name
        db_game.genre = game.genre
        db_game.platform = game.platform
        db_game.released_year = game.released_year
        db_game.allow_multiplayer = game.allow_multiplayer
        db.add(db_game)
        db.commit()
        db.refresh(db_game)
        return db_game
