from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.domain.exceptions import BusinessRuleException


class BusinessRuleMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except BusinessRuleException as e:
            return JSONResponse(
                status_code=200,
                content={
                    "errors": [
                        {"message": e.message, "extensions": {"code": e.code}}
                    ],
                    "data": None,
                },
            )
