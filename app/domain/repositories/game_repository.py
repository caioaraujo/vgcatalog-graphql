from abc import ABC, abstractmethod

from app.infra.database.models import Game
from app.schemas.game import GameList


class GameRepository(ABC):

    @abstractmethod
    def get_by_name_and_platform(self, name: str, platform: str):
        pass

    @abstractmethod
    def create_or_update(self, game: Game):
        pass

    @abstractmethod
    def get_by_id(self, game_id: int):
        pass

    @abstractmethod
    def get_by_filter(self, filters: GameList):
        pass
