from app.domain.exceptions import GameAlreadyExistsException, GameNotFoundException
from app.domain.models import Game
from app.repositories.game_repository import GameRepository
from app.schemas.game import GameCreate


class GameService:
    def __init__(self, repository: GameRepository):
        self.repository = repository

    def create_game(self, game: GameCreate):
        existing = self.repository.get_by_name_and_platform(game.name, game.platform)
        if existing:
            raise GameAlreadyExistsException()

        db_game = Game(
            name=game.name,
            released_year=game.released_year,
            platform=game.platform,
            genre=game.genre,
            allow_multiplayer=game.allow_multiplayer,
        )
        return self.repository.create_or_update(db_game)

    def update_game(self, game_id: int, game: GameCreate):
        db_game = self.repository.get_by_id(game_id)
        if not db_game:
            raise GameNotFoundException()
        db_game.name = game.name
        db_game.genre = game.genre
        db_game.platform = game.platform
        db_game.released_year = game.released_year
        db_game.allow_multiplayer = game.allow_multiplayer
        return self.repository.create_or_update(db_game)

    def fetch_game(self, game_id: int):
        game = self.repository.get_by_id(game_id)
        if not game:
            raise GameNotFoundException()
        return game
