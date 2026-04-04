from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.domain.services.game_service import GameService
from app.infra.repositories.game_repository_impl import GameRepositoryImpl


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_context(db: Session = Depends(get_db)):
    return {"db": db, "game_service": GameService(GameRepositoryImpl(db))}
