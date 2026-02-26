import pytest
from unittest.mock import MagicMock

from app.models.game import Game as GameModel
from app.schemas.game import Game, GameCreate
from app.services.game_service import GameService


@pytest.fixture
def db_mock():
    return MagicMock()


@pytest.fixture
def game_create_data():
    return GameCreate(
        name="Super Mario World",
        released_year=1990,
        platform="Super Nintendo",
        genre="2D Platform",
        allow_multiplayer=True,
    )


@pytest.fixture
def game_update_data():
    return GameCreate(
        name="Final Fantasy VII",
        released_year=1997,
        platform="Playstation",
        genre="JRPG",
        allow_multiplayer=False,
    )


@pytest.fixture
def game_retrieve_data():
    return Game(
        id=1000,
        name="FinalFantasyVII",
        released_year=1993,
        platform="Playstation 2",
        genre="Action RPG",
        allow_multiplayer=True,
    )


def test_create_game(db_mock, game_create_data):
    service = GameService()

    result = service.create_game(db_mock, game_create_data)

    db_mock.add.assert_called_once()
    db_mock.commit.assert_called_once()
    db_mock.refresh.assert_called_once()

    assert result.name == "Super Mario World"
    assert result.released_year == 1990
    assert result.platform == "Super Nintendo"
    assert result.genre == "2D Platform"
    assert result.allow_multiplayer is True


def test_update_game_when_game_exists(db_mock, game_update_data, game_retrieve_data):
    service = GameService()
    db_mock.get.return_value = game_retrieve_data

    result = service.update_game(db_mock, game_id=1000, game=game_update_data)

    db_mock.get.assert_called_once_with(GameModel, 1000)
    assert result.id == 1000
    assert result.name == "Final Fantasy VII"
    assert result.released_year == 1997
    assert result.platform == "Playstation"
    assert result.genre == "JRPG"
    assert result.allow_multiplayer is False


def test_update_game_when_game_does_not_exists(db_mock, game_update_data):
    service = GameService()
    db_mock.get.return_value = None

    result = service.update_game(db_mock, game_id=9999, game=game_update_data)

    db_mock.get.assert_called_once_with(GameModel, 9999)
    assert result is None
