from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Annotated

from sqlmodel import select
from models.user import User, Token, TokenData
from appglobals import SessionDep, oauth2_scheme
from sqlmodel import Session
import uuid
from datetime import datetime, timedelta, UTC
from jose import JWTError, jwt

SECRET_KEY = "binky"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 360

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user_from_token(token, session: Session):
    user = session.exec(select(User).where(User.id == token)).first()
    return user


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        userid: str = payload.get("sub")
        if userid is None:
            raise credentials_exception
        token_data = TokenData(userid=userid)
    except JWTError:
        raise credentials_exception
    user = session.exec(select(User).where(User.id == token_data.userid)).first()
    if user is None:
        raise credentials_exception
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/token", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep
) -> Token:
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    # user_dict = session.exec(select(User).filter(offset).limit(limit)).all() form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # hashed_password = form_data.password
    # if not hashed_password == user.hashed_password:
    #     raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    return current_user


@router.post("/users/register", response_model=User)
async def register_new_user(
    user: User,
    current_user: Annotated[User, Depends(get_current_user)],
    session: SessionDep,
) -> User:

    if current_user.username != "thibaut":
        raise HTTPException(status_code=401, detail="not authorzied")

    if user.id == None:
        user.id = str(uuid.uuid4())
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


# @router.post("/users/{name}/overridePassword")
# async def override_password(
#     name: str, newpassword: str, token: Annotated[str, Depends(oauth2_scheme)]
# ):
#     ##todo verify that itsa me
#     ##get user update pw
#     return {"message": "password updated successfully"}
