import pytest
from unittest.mock import MagicMock

from app.schemas.game import Game, GameCreate


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


@pytest.fixture
def repository_create_game_is_new_mock():
    mock_repo = MagicMock()
    mock_repo.get_by_name_and_platform.return_value = None
    mock_repo.create_or_update.return_value = Game(
        id=1,
        name="Super Mario World",
        released_year=1990,
        platform="Super Nintendo",
        genre="2D Platform",
        allow_multiplayer=True,
    )
    return mock_repo


@pytest.fixture
def repository_create_game_already_exists_mock(game_retrieve_data):
    mock_repo = MagicMock()
    mock_repo.get_by_name_and_platform.return_value = game_retrieve_data
    return mock_repo


@pytest.fixture
def repository_update_game_exists_mock(game_retrieve_data):
    mock_repo = MagicMock()
    mock_repo.get_by_id.return_value = game_retrieve_data
    mock_repo.create_or_update.return_value = Game(
        id=1000,
        name="Final Fantasy VII",
        released_year=1997,
        platform="Playstation",
        genre="JRPG",
        allow_multiplayer=False,
    )
    return mock_repo


@pytest.fixture
def repository_update_game_not_exists_mock(game_retrieve_data):
    mock_repo = MagicMock()
    mock_repo.get_by_id.return_value = None
    return mock_repo
