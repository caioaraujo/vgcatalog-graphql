import datetime

from fastapi import Depends
from sqlalchemy.orm import Session

from app.infra.db.database import SessionLocal
from app.application.services.game_service import GameService
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


def get_context(db: Session = Depends(get_db)):
    return {"db": db, "game_service": GameService(GameRepositoryImpl(db, Clock()))}
