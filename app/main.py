from fastapi import FastAPI, Depends
from starlette.responses import JSONResponse
from strawberry.fastapi import GraphQLRouter

from .dependencies import get_db
from .domain.exceptions import GameAlreadyExistsException, GameNotFoundException
from app.api.graphql import schema
from .api.rest import games

app = FastAPI(title="VGCatalog")

graphql_app = GraphQLRouter(schema, context_getter=lambda db=Depends(get_db): {"db": db})

app.include_router(graphql_app, prefix="/graphql", tags=["GraphQL"])
app.include_router(games.router, tags=["REST"])


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
