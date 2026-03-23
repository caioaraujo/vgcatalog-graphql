from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.repositories.game_repository import GameRepository
from app.services.game_service import GameService


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_context(db: Session = Depends(get_db)):
    return {"db": db, "game_service": GameService(GameRepository(db))}
