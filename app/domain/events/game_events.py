from app.core.config import Topics


class GameCreatedEvent:

    name = Topics.GAME_CREATED

    def __init__(self, game):
        self.payload = {
            "id": game.id,
            "name": game.name,
            "released_year": game.released_year,
            "platform": game.platform,
            "genre": game.genre,
            "allow_multiplayer": game.allow_multiplayer,
            "created_at": game.created_at,
        }
