import pytest

from app.domain.models import Game
from app.repositories.game_repository import GameRepository
from app.schemas.game import GameList, StringFilter, IntFilter, BooleanFilter


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


def test_get_by_filter_by_name_and_platform(db_session, games_factory):
    games_factory.create_batch(2)
    repository = GameRepository(db_session)
    game_filter = GameList(
        name=StringFilter(eq="Game 1"), platform=StringFilter(eq="Super Nintendo")
    )
    result = repository.get_by_filter(game_filter)
    assert len(result) == 1
    game = result[0]
    assert game.name == "Game 1"
    assert game.platform == "Super Nintendo"


def test_get_by_filter_by_name_equals(db_session, games_factory):
    games_factory.create_batch(2)
    repository = GameRepository(db_session)
    game_filter = GameList(name=StringFilter(eq="Game 1"))
    result = repository.get_by_filter(game_filter)
    assert len(result) == 1
    game = result[0]
    assert game.name == "Game 1"


def test_get_by_filter_by_name_contains(db_session, games_factory):
    games_factory.create_batch(2)
    repository = GameRepository(db_session)
    game_filter = GameList(name=StringFilter(contains="Game"))
    result = repository.get_by_filter(game_filter)
    assert len(result) == 2
    assert all(("Game" in game.name for game in result))


def test_get_by_filter_by_name_in_list(db_session, games_factory):
    games_factory.create_batch(3)
    repository = GameRepository(db_session)
    game_filter = GameList(name=StringFilter(in_list=["Game 1", "Game 2"]))
    result = repository.get_by_filter(game_filter)
    assert len(result) == 2


@pytest.mark.parametrize("released_year,len_expected", [(1991, 5), (1992, 0)])
def test_get_by_filter_by_release_year(
    db_session, games_factory, released_year, len_expected
):
    games_factory.create_batch(5)
    repository = GameRepository(db_session)
    game_filter = GameList(released_year=IntFilter(eq=released_year))
    result = repository.get_by_filter(game_filter)
    assert len(result) == len_expected


def test_get_by_genre(db_session, games_factory):
    games_factory.create_batch(2)
    repository = GameRepository(db_session)
    game_filter = GameList(genre=StringFilter(eq="Beat Em Up"))
    result = repository.get_by_filter(game_filter)
    assert len(result) == 2
    assert all((game.genre == "Beat Em Up" for game in result))


@pytest.mark.parametrize("allow_multiplayer,len_expected", [(True, 5), (False, 0)])
def test_get_by_filter_by_allow_multiplayer(
    db_session, games_factory, allow_multiplayer, len_expected
):
    games_factory.create_batch(5)
    repository = GameRepository(db_session)
    game_filter = GameList(allow_multiplayer=BooleanFilter(eq=allow_multiplayer))
    result = repository.get_by_filter(game_filter)
    assert len(result) == len_expected
