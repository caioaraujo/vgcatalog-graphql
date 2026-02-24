import pytest
from unittest.mock import MagicMock

from app.schemas.game import GameCreate
from app.services.game_service import GameService


@pytest.fixture
def db_mock():
    return MagicMock()


@pytest.fixture
def game_data():
    return GameCreate(
        name="Super Mario World",
        released_year=1990,
        platform="Super Nintendo",
        genre="2D Platform",
        allow_multiplayer=True,
    )


def test_create_game(db_mock, game_data):
    service = GameService()

    result = service.create_game(db_mock, game_data)

    db_mock.add.assert_called_once()
    db_mock.commit.assert_called_once()
    db_mock.refresh.assert_called_once()

    assert result.name == "Super Mario World"
    assert result.released_year == 1990
    assert result.platform == "Super Nintendo"
    assert result.genre == "2D Platform"
    assert result.allow_multiplayer is True
