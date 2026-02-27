import pytest
from unittest.mock import MagicMock

from app.dependencies import get_db


def test_get_db_yields_session_and_closes(monkeypatch):
    mock_session = MagicMock()
    mock_session.close = MagicMock()

    monkeypatch.setattr(
        "app.dependencies.SessionLocal",
        lambda: mock_session
    )

    generator = get_db()

    db = next(generator)

    assert db == mock_session

    with pytest.raises(StopIteration):
        next(generator)

    mock_session.close.assert_called_once()
