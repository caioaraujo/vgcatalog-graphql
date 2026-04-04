import datetime

import factory.alchemy
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.infra.repositories.game_repository_impl import GameRepositoryImpl
from app.main import app
from app.infra.db.database import Base
from app.core.dependencies import get_db, get_event_bus
from app.infra.orm.models.game import Game


class FakeEventBus:
    def __init__(self):
        self.events = []

    def publish(self, event_type: str, payload: dict):
        self.events.append(
            {
                "event_type": event_type,
                "payload": payload,
            }
        )

    def assert_event(self, event_type: str, **expected_payload):
        for event in self.events:
            if event["event_type"] == event_type:
                for key, value in expected_payload.items():
                    if key == "created_at":
                        assert isinstance(event["payload"][key], datetime.datetime)
                    else:
                        assert event["payload"][key] == value
                return
        assert False, f"Event {event_type} not published"


@pytest.fixture
def fake_event_bus():
    return FakeEventBus()


@pytest.fixture
def engine(postgresql):
    db_url = (
        f"postgresql+psycopg2://{postgresql.info.user}:"
        f"@{postgresql.info.host}:"
        f"{postgresql.info.port}/"
        f"{postgresql.info.dbname}"
    )

    engine = create_engine(db_url)

    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture
def db_session(engine):
    connection = engine.connect()
    transaction = connection.begin()

    TestingSessionLocal = sessionmaker(bind=connection)
    session = TestingSessionLocal()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session, fake_event_bus):
    def override_get_db():
        yield db_session

    def override_get_event_bus():
        return fake_event_bus

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_event_bus] = override_get_event_bus

    yield TestClient(app)

    app.dependency_overrides.clear()


class FakeClock:
    def now(self):
        return datetime.datetime(2026, 1, 1, 3, 21, 34)


@pytest.fixture
def repository(db_session):
    return GameRepositoryImpl(db_session, FakeClock())


@pytest.fixture
def game_factory(db_session):
    class _GameFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = Game
            sqlalchemy_session = db_session
            sqlalchemy_session_persistence = "commit"

        id = 2
        name = "Teenage Mutant Ninja Turtles: Turtles in Time"
        platform = "Super Nintendo"
        genre = "BeatEm Up"
        released_year = 1991
        allow_multiplayer = True
        created_at = datetime.datetime(2025, 1, 1, 3, 21, 34)

    return _GameFactory


@pytest.fixture
def games_factory(db_session):
    class _GameFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = Game
            sqlalchemy_session = db_session
            sqlalchemy_session_persistence = "commit"

        id = factory.Sequence(lambda n: n + 1)
        name = factory.Sequence(lambda n: f"Game {n}")
        platform = "Super Nintendo"
        genre = "Beat Em Up"
        released_year = 1991
        allow_multiplayer = True

    return _GameFactory
