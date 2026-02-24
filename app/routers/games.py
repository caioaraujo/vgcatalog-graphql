from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.game import GameCreate
from app.services.game_service import GameService

router = APIRouter(prefix="/games", tags=["games"])


@router.get("/")
async def read_games():
    return [
        {
            "id": 1,
            "name": "Super Mario World",
            "released_year": 1990,
            "platform": "Super Nintendo",
            "genre": "2D Platform",
            "allow_multiplayer": True,
        }
    ]


@router.get("/{game_id}")
async def read_game_by_id(game_id: int):
    return {
        "id": game_id,
    }


@router.put("/{game_id}")
async def update_game(game_id: int):
    pass


@router.post("/", response_model=GameCreate)
async def create_game(game: GameCreate, db: Session = Depends(get_db)):
    return GameService().create_game(db, game)
