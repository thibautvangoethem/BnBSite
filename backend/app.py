from fastapi import FastAPI
from sqlmodel import SQLModel
from contextlib import asynccontextmanager

import logging
from fastapi.middleware.cors import CORSMiddleware
import os

from endpoints import authentication, hero
from appglobals import engine

LOG = logging.getLogger(__name__)

origins = [
    # "http://localhost",
    "*",
]
if "VITE_FRONTEND_URL" in os.environ:
    # origins.append(str(os.environ["VITE_FRONTEND_URL"]))
    pass
else:
    LOG.info("FAILING")
    LOG.info(str(origins))


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(authentication.router)
app.include_router(hero.router)


app = CORSMiddleware(
    app=app,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
