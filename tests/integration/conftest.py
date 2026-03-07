import factory.alchemy
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.db.database import Base
from app.dependencies import get_db
from app.domain.models import Game


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
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

    app.dependency_overrides.clear()


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
