from app.domain.models import Game
from app.repositories.game_repository import GameRepository


def test_get_by_name_and_platform_when_game_exists(db_session, game_factory):
    game_factory()
    repository = GameRepository(db_session)
    name = "Teenage Mutant Ninja Turtles: Turtles in Time"
    platform = "Super Nintendo"

    result = repository.get_by_name_and_platform(name, platform)

    assert result.name == name
    assert result.platform == platform


def test_get_by_name_and_platform_when_game_does_not_exists(db_session):
    repository = GameRepository(db_session)
    name = "Sonic the Hedgehog"
    platform = "Mega Drive"

    result = repository.get_by_name_and_platform(name, platform)

    assert result is None


def test_create_or_update_when_create(db_session):
    repository = GameRepository(db_session)
    game = Game()
    game.name = "Aladdin"
    game.genre = "2D Platform"
    game.released_year = 1993
    game.platform = "Super Nintendo"
    game.allow_multiplayer = False

    result = repository.create_or_update(game)

    assert result.id is not None
    assert result.name == game.name
    assert result.genre == game.genre
    assert result.platform == game.platform
    assert result.released_year == game.released_year
    assert result.allow_multiplayer == game.allow_multiplayer


def test_create_or_update_when_update(db_session, game_factory):
    game_factory()
    repository = GameRepository(db_session)
    game = db_session.get(Game, 2)
    game.name = "TMNT IV"
    game.genre = "Beat em Up"
    game.released_year = 1992
    game.platform = "Super Nintendo"
    game.allow_multiplayer = True

    result = repository.create_or_update(game)

    assert result.id == game.id
    assert result.name == game.name
    assert result.genre == game.genre
    assert result.platform == game.platform
    assert result.released_year == game.released_year
    assert result.allow_multiplayer == game.allow_multiplayer


def test_get_by_id_when_game_exists(db_session, game_factory):
    game_factory()
    repository = GameRepository(db_session)
    result = repository.get_by_id(2)

    assert result.id == 2
    assert result.name == "Teenage Mutant Ninja Turtles: Turtles in Time"
    assert result.platform == "Super Nintendo"


def test_get_by_id_when_game_does_not_exists(db_session):
    repository = GameRepository(db_session)
    result = repository.get_by_id(1)

    assert result is None
