from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.repositories.game_repository import GameRepository
from app.schemas.game import Game, GameCreate
from app.services.game_service import GameService

router = APIRouter(prefix="/games", tags=["games"])


@router.get("/")
def read_games():
    # FIXME
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
def read_game_by_id(game_id: int, db: Session = Depends(get_db)):
    repository = GameRepository(db)
    return GameService(repository).fetch_game(game_id)


@router.put("/{game_id}", response_model=Game)
def update_game(game_id: int, game: GameCreate, db: Session = Depends(get_db)):
    repository = GameRepository(db)
    return GameService(repository).update_game(game_id, game)


@router.post("/", response_model=GameCreate)
def create_game(game: GameCreate, db: Session = Depends(get_db)):
    repository = GameRepository(db)
    game = GameService(repository).create_game(game)
    return game
