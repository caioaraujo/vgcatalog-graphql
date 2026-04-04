def game_created_event(game) -> dict:
    return {
        "id": game.id,
        "name": game.name,
        "released_year": game.released_year,
        "platform": game.platform,
        "genre": game.genre,
        "allow_multiplayer": game.allow_multiplayer,
        "created_at": game.created_at,
    }
