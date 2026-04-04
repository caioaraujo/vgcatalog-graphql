import datetime

import pytest

from app.infra.orm.models import Game
from app.schemas.game import (
    GameList,
    StringFilter,
    IntFilter,
    BooleanFilter,
    PaginationInput,
    SortInput,
)


def test_get_by_name_and_platform__when_game_exists(repository, game_factory):
    # Arrange
    game_factory()
    name = "Teenage Mutant Ninja Turtles: Turtles in Time"
    platform = "Super Nintendo"

    # Act
    result = repository.get_by_name_and_platform(name, platform)

    # Assert
    assert result.name == name
    assert result.platform == platform


def test_get_by_name_and_platform__when_game_does_not_exists(repository):
    # Arrange
    name = "Sonic the Hedgehog"
    platform = "Mega Drive"

    # Act
    result = repository.get_by_name_and_platform(name, platform)

    # Assert
    assert result is None


def test_create_or_update__when_create(repository):
    # Arrange
    game = Game()
    game.name = "Aladdin"
    game.genre = "2D Platform"
    game.released_year = 1993
    game.platform = "Super Nintendo"
    game.allow_multiplayer = False

    # Act
    result = repository.create_or_update(game)

    # Assert
    assert result.id is not None
    assert result.name == game.name
    assert result.genre == game.genre
    assert result.platform == game.platform
    assert result.released_year == game.released_year
    assert result.allow_multiplayer == game.allow_multiplayer
    assert result.created_at == datetime.datetime(2026, 1, 1, 3, 21, 34)


def test_create_or_update__when_update(repository, db_session, game_factory):
    # Arrange
    game_factory()
    game = db_session.get(Game, 2)
    game.name = "TMNT IV"
    game.genre = "Beat em Up"
    game.released_year = 1992
    game.platform = "Super Nintendo"
    game.allow_multiplayer = True

    # Act
    result = repository.create_or_update(game)

    # Assert
    assert result.id == game.id
    assert result.name == game.name
    assert result.genre == game.genre
    assert result.platform == game.platform
    assert result.released_year == game.released_year
    assert result.allow_multiplayer == game.allow_multiplayer
    assert result.created_at == datetime.datetime(2025, 1, 1, 3, 21, 34)


def test_get_by_id__when_game_exists(repository, game_factory):
    # Arrange
    game_factory()

    # Act
    result = repository.get_by_id(2)

    # Assert
    assert result.id == 2
    assert result.name == "Teenage Mutant Ninja Turtles: Turtles in Time"
    assert result.platform == "Super Nintendo"


def test_get_by_id__when_game_does_not_exists(repository):
    # Arrange
    game_id = 1

    # Act
    result = repository.get_by_id(game_id)

    # Assert
    assert result is None


def test_get_by_filter__when_filter_by_name_and_platform__returns_one_value(
    repository, games_factory
):
    # Arrange
    games_factory.create(name="Game 1", platform="Super Nintendo")
    games_factory.create(name="Game 1", platform="Mega Drive")
    game_filter = GameList(
        name=StringFilter(eq="Game 1"), platform=StringFilter(eq="Super Nintendo")
    )

    # Act
    result = repository.get_by_filter(game_filter)

    # Assert
    assert len(result) == 1
    game = result[0]
    assert game.name == "Game 1"
    assert game.platform == "Super Nintendo"


def test_get_by_filter__when_filter_by_name_equals__returns_one_value(
    repository, games_factory
):
    # Arrange
    games_factory.create(name="Game 1")
    games_factory.create(name="Game 2")
    game_filter = GameList(name=StringFilter(eq="Game 1"))

    # Act
    result = repository.get_by_filter(game_filter)

    # Assert
    assert len(result) == 1
    assert result[0].name == "Game 1"


def test_get_by_filter__when_filter_by_name_contains__returns_two_values(
    repository, games_factory
):
    # Arrange
    games_factory.create_batch(2)
    game_filter = GameList(name=StringFilter(contains="Game"))

    # Act
    result = repository.get_by_filter(game_filter)

    # Assert
    assert len(result) == 2
    assert all(("Game" in game.name for game in result))


def test_get_by_filter__when_filter_by_name_in_list__returns_two_values(
    repository, games_factory
):
    # Arrange
    games_factory.create(name="Game 1")
    games_factory.create(name="Game 2")
    games_factory.create(name="Game 3")
    game_filter = GameList(name=StringFilter(in_list=["Game 1", "Game 2", "Game 4"]))

    # Act
    result = repository.get_by_filter(game_filter)

    # Assert
    assert len(result) == 2


@pytest.mark.parametrize("released_year,len_expected", [(1991, 5), (1992, 0)])
def test_get_by_filter__when_filter_by_release_year_equals__returns_zero_to_many_values(
    repository, games_factory, released_year, len_expected
):
    # Arrange
    games_factory.create(name="Street Fighter II: Champion Edition", released_year=1991)
    games_factory.create(name="Sunset Riders", released_year=1991)
    games_factory.create(name="Sonic the Hedgehog", released_year=1991)
    games_factory.create(name="Battletoads", released_year=1991)
    games_factory.create(name="Mega Man 4", released_year=1991)

    game_filter = GameList(released_year=IntFilter(eq=released_year))

    # Act
    result = repository.get_by_filter(game_filter)

    # Assert
    assert len(result) == len_expected


@pytest.mark.parametrize("released_year,len_expected", [(1990, 5), (1991, 0)])
def test_get_by_filter__when_filter_by_release_year_gt__returns_zero_to_many_values(
    repository, games_factory, released_year, len_expected
):
    # Arrange
    games_factory.create(name="Street Fighter II: Champion Edition", released_year=1991)
    games_factory.create(name="Sunset Riders", released_year=1991)
    games_factory.create(name="Sonic the Hedgehog", released_year=1991)
    games_factory.create(name="Battletoads", released_year=1991)
    games_factory.create(name="Mega Man 4", released_year=1991)
    game_filter = GameList(released_year=IntFilter(gt=released_year))

    # Act
    result = repository.get_by_filter(game_filter)

    # Assert
    assert len(result) == len_expected


@pytest.mark.parametrize("released_year,len_expected", [(1991, 0), (1992, 5)])
def test_get_by_filter__when_filter_by_release_year_lt__returns_zero_to_many_values(
    repository, games_factory, released_year, len_expected
):
    # Arrange
    games_factory.create(name="Street Fighter II: Champion Edition", released_year=1991)
    games_factory.create(name="Sunset Riders", released_year=1991)
    games_factory.create(name="Sonic the Hedgehog", released_year=1991)
    games_factory.create(name="Battletoads", released_year=1991)
    games_factory.create(name="Mega Man 4", released_year=1991)
    game_filter = GameList(released_year=IntFilter(lt=released_year))

    # Act
    result = repository.get_by_filter(game_filter)

    # Assert
    assert len(result) == len_expected


def test_get_by_filter__when_filter_by_genre_equals__returns_two_values(
    repository, games_factory
):
    # Arrange
    games_factory.create(name="Battletoads", genre="Beat Em Up")
    games_factory.create(name="Final Fight", genre="Beat Em Up")
    game_filter = GameList(genre=StringFilter(eq="Beat Em Up"))

    # Act
    result = repository.get_by_filter(game_filter)

    # Assert
    assert len(result) == 2
    assert all((game.genre == "Beat Em Up" for game in result))


@pytest.mark.parametrize("allow_multiplayer,len_expected", [(True, 3), (False, 0)])
def test_get_by_filter__when_filter_by_allow_multiplayer__returns_zero_to_many_values(
    repository, games_factory, allow_multiplayer, len_expected
):
    # Arrange
    games_factory.create(name="Battletoads", allow_multiplayer=True)
    games_factory.create(name="Super Mario World", allow_multiplayer=True)
    games_factory.create(name="Mortal Kombat", allow_multiplayer=True)
    game_filter = GameList(allow_multiplayer=BooleanFilter(eq=allow_multiplayer))

    # Act
    result = repository.get_by_filter(game_filter)

    # Assert
    assert len(result) == len_expected


def test_get_by_filter__when_has_no_filter__returns_all_values(
    repository, games_factory
):
    # Arrange
    games_factory.create_batch(5)
    game_filter = GameList()

    # Act
    result = repository.get_by_filter(game_filter)

    # Assert
    assert len(result) == 5


def test_get_by_filter__when_using_pagination__returns_twenty_values(
    repository, games_factory
):
    # Arrange
    games_factory.create_batch(50)
    game_filter = GameList(pagination=PaginationInput(limit=20, offset=2))

    # Act
    result = repository.get_by_filter(game_filter)

    # Assert
    assert len(result) == 20


@pytest.mark.parametrize(
    "direction,first_game,last_game",
    [("desc", "Zoop", "Aero the Acrobat"), ("asc", "Aero the Acrobat", "Zoop")],
)
def test_get_by_filter__when_using_sort__returns_five_values(
    repository, games_factory, direction, first_game, last_game
):
    # Arrange
    games_factory.create(name="Aero the Acrobat")
    games_factory.create(name="Zoop")
    games_factory.create(name="Comix Zone")
    games_factory.create(name="Super Star Wars")
    games_factory.create(name="Final Fantasy VI")
    game_filter = GameList(sort=SortInput(field="name", direction=direction))

    # Act
    result = repository.get_by_filter(game_filter)

    # Assert
    assert len(result) == 5
    assert result[0].name == first_game
    assert result[-1].name == last_game
