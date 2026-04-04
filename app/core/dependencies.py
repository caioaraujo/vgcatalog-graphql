import datetime

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.config import KAFKA_BOOTSTRAP_SERVER
from app.infra.db.database import SessionLocal
from app.application.services.game_service import GameService
from app.infra.messaging.event_bus_impl import KafkaEventBus
from app.infra.repositories.game_repository_impl import GameRepositoryImpl


class Clock:
    def now(self):
        return datetime.datetime.now()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_event_bus() -> KafkaEventBus:
    return KafkaEventBus(bootstrap_server=KAFKA_BOOTSTRAP_SERVER)


def get_context(db: Session = Depends(get_db), event_bus=Depends(get_event_bus)):
    repository = GameRepositoryImpl(db, Clock())
    return {"db": db, "game_service": GameService(repository, event_bus)}
