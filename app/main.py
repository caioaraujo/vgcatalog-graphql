from fastapi import FastAPI
from starlette.responses import JSONResponse

from .domain.exceptions import GameAlreadyExistsException, GameNotFoundException
from .routers import games

app = FastAPI()

app.include_router(games.router)


@app.exception_handler(GameAlreadyExistsException)
def handle_game_exists(_, __):
    return JSONResponse(
        status_code=400,
        content={"detail": "Game already exists for the given platform"},
    )


@app.exception_handler(GameNotFoundException)
def handle_game_not_found(_, __):
    return JSONResponse(
        status_code=404,
        content={"detail": "Game not exists"},
    )
