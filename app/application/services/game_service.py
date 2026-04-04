from typing import List

from app.domain.events.event_bus import EventBus
from app.domain.events.game_events import GameCreatedEvent
from app.domain.exceptions import GameAlreadyExistsException, GameNotFoundException
from app.infra.orm.models.game import Game
from app.domain.repositories.game_repository import GameRepository
from app.schemas.game import GameCreate


class GameService:
    def __init__(self, repository: GameRepository, event_bus: EventBus):
        self.repository = repository
        self.event_bus = event_bus

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

        # Persist in DB
        game = self.repository.create_or_update(db_game)

        # Send to event bus
        event = GameCreatedEvent(game)
        self.event_bus.publish(event.name, event.payload)

        return game

    def update_game(self, game_id: int, game: GameCreate):
        db_game = self.repository.get_by_id(game_id)
        if not db_game:
            raise GameNotFoundException()
        existed_game_for_platform = self.repository.get_by_name_and_platform(
            game.name, game.platform
        )
        if existed_game_for_platform and existed_game_for_platform.id != game_id:
            raise GameAlreadyExistsException()
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

    def list_games(self, game_filter: List):
        return self.repository.get_by_filter(game_filter)
