from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, create_engine
from typing import Annotated
import os
import logging

LOG = logging.getLogger(__name__)

connect_args = {"check_same_thread": False}
DATABASE_URL = "bwaha hier staat niets nuttig"
if "DATABASE_URL" in os.environ:
    DATABASE_URL = os.environ["DATABASE_URL"]
else:
    # DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:5432/bnbsite"
    LOG.info("WARNING, DATABASE_URL environ not found, assuming local execution")

engine = create_engine(DATABASE_URL, echo=True)


# dependency for database calls
def get_session():
    with Session(engine) as session:
        yield session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SessionDep = Annotated[Session, Depends(get_session)]
