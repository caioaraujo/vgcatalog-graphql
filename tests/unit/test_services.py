import pytest

from app.domain.exceptions import GameAlreadyExistsException, GameNotFoundException
from app.services.game_service import GameService


def test_create_game_when_game_is_new(game_create_data, repository_create_game_is_new_mock):
    service = GameService(repository_create_game_is_new_mock)

    result = service.create_game(game_create_data)

    repository_create_game_is_new_mock.get_by_name_and_platform.assert_called_once()
    repository_create_game_is_new_mock.create_or_update.assert_called_once()

    assert result.name == "Super Mario World"
    assert result.released_year == 1990
    assert result.platform == "Super Nintendo"
    assert result.genre == "2D Platform"
    assert result.allow_multiplayer is True


def test_create_game_when_game_already_exists(game_create_data, repository_create_game_already_exists_mock):
    service = GameService(repository_create_game_already_exists_mock)

    with pytest.raises(GameAlreadyExistsException):
        service.create_game(game_create_data)

    repository_create_game_already_exists_mock.get_by_name_and_platform.assert_called_once()


def test_update_game_when_game_exists(
    game_update_data, repository_update_game_exists_mock
):
    service = GameService(repository_update_game_exists_mock)

    result = service.update_game(game_id=1000, game=game_update_data)

    repository_update_game_exists_mock.get_by_id.assert_called_once_with(1000)
    repository_update_game_exists_mock.create_or_update.assert_called_once()

    assert result.id == 1000
    assert result.name == "Final Fantasy VII"
    assert result.released_year == 1997
    assert result.platform == "Playstation"
    assert result.genre == "JRPG"
    assert result.allow_multiplayer is False


def test_update_game_when_game_does_not_exists(
    game_update_data, repository_get_by_id_game_not_exists_mock
):
    service = GameService(repository_get_by_id_game_not_exists_mock)

    with pytest.raises(GameNotFoundException):
        service.update_game(game_id=9999, game=game_update_data)

    repository_get_by_id_game_not_exists_mock.get_by_id.assert_called_once_with(9999)


def test_fetch_game_when_game_does_not_exists(repository_get_by_id_game_not_exists_mock):
    service = GameService(repository_get_by_id_game_not_exists_mock)

    with pytest.raises(GameNotFoundException):
        service.fetch_game(game_id=9999)

    repository_get_by_id_game_not_exists_mock.get_by_id.assert_called_once_with(9999)


def test_fetch_game_when_game_exists(repository_get_by_id_game_exists_mock):
    service = GameService(repository_get_by_id_game_exists_mock)

    result = service.fetch_game(game_id=1000)

    assert result.id == 1000
    assert result.name == "FinalFantasyVII"

    repository_get_by_id_game_exists_mock.get_by_id.assert_called_once_with(1000)
