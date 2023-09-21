from fastapi import FastAPI

from .authentication import router
from .authorization import flight_router

app = FastAPI()

app.include_router(router)
app.include_router(flight_router)
