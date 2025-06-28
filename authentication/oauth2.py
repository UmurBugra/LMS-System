from fastapi import Depends, HTTPException, status, Cookie
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from db.database import get_db
from crud.login import get_user_by_email_and_id, create_user_with_auth
from crud.calendar import create_calendar_by_auth
from schemas import UserType

SECRET_KEY = 'd68209ffa66480a47408acdc06f3d35016a7e3dfbbec769592ccd9e56d97ba7e'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Not authenticated",
    headers={"WWW-Authenticate": "Bearer"},
)


# Token oluşturucu
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Cookie'den token okuyarak kullanıcıyı döner
def get_current_user_from_cookie(
    access_token: Optional[str] = Cookie(None),
    db: Session = Depends(get_db)
):
    if access_token is None:
        raise credentials_exception
    try:
        token = access_token.replace("Bearer ", "")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        if email is None or user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_email_and_id(db, email, user_id)
    if user is None:
        raise credentials_exception
    return user


# Calendar yetkilendirme (cookie üzerinden)
def create_authentication_token(
    access_token: Optional[str] = Cookie(None),
    db: Session = Depends(get_db)
):
    if access_token is None:
        raise credentials_exception
    try:
        token = access_token.replace("Bearer ", "")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = create_calendar_by_auth(db, username, user_type=UserType.teacher)
    if user is None:
        raise credentials_exception
    return user


# Kullanıcı oluşturma (cookie üzerinden)
def create_user_authentication_token(
    access_token: Optional[str] = Cookie(None),
    db: Session = Depends(get_db)
):
    if access_token is None:
        raise credentials_exception
    try:
        token = access_token.replace("Bearer ", "")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = create_user_with_auth(db, username, user_type=UserType.teacher)
    if user is None:
        raise credentials_exception
    return user

def student_authentication_token(
    access_token: Optional[str] = Cookie(None),
    db: Session = Depends(get_db)
):
    if access_token is None:
        raise credentials_exception
    try:
        token = access_token.replace("Bearer ", "")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_username(db, username)
    if user is None or user.type != UserType.student:
        raise credentials_exception
    return user