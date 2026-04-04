from fastapi import FastAPI
from starlette.responses import JSONResponse
from strawberry.fastapi import GraphQLRouter

from app.interfaces.graphql.middleware import BusinessRuleMiddleware
from app.core.dependencies import get_context
from app.domain.exceptions import GameAlreadyExistsException, GameNotFoundException
from app.interfaces.graphql.schema import schema

app = FastAPI(title="VGCatalog")
app.add_middleware(BusinessRuleMiddleware)

graphql_app = GraphQLRouter(schema, context_getter=get_context)

app.include_router(graphql_app, prefix="/graphql/games", tags=["GraphQL"])


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
