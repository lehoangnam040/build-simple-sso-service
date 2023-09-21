from fastapi import APIRouter, Depends, Security

from .middlewares import scope_authorization_middleware

flight_router = APIRouter()

@flight_router.get("/v1/flights")
async def get_flights(
    _ = Security(
        scope_authorization_middleware,
        scopes=["flights:list",],
    ),
):
    return [1, 2, 3, 4]


@flight_router.post("/v1/flights")
async def create_flights(
    _ = Security(
        scope_authorization_middleware,
        scopes=["flights:create",],
    ),
):
    return {
        "status": "OK"
    }

@flight_router.patch("/v1/flights")
async def modify_flights(
    _ = Security(
        scope_authorization_middleware,
        scopes=["flights:modify",],
    ),
):
    return {
        "status": "OK"
    }