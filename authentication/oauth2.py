from fastapi import Depends, HTTPException, status, Cookie
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import LoginData
from crud.login import get_user_by_email_and_id, get_user_student
from crud.calendar import create_calendar_by_auth
from schemas import UserType

SECRET_KEY = 'd68209ffa66480a47408acdc06f3d35016a7e3dfbbec769592ccd9e56d97ba7e' # --> openssl rand -hex 32
ALGORITHM = 'HS256' # --> HMAC-SHA256 algoritması
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # --> Token'ın geçerlilik süresi (dakika cinsinden)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") # --> OAuth2PasswordBearer bir endpointten token almayı sağlar
                                                       # --> /token endpointi, token almak için kullanılacak

credentials_exception = HTTPException(                 # --> Doğrulama başarısız olduğunda döndürülür (401)
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Not authenticated",
    headers={"WWW-Authenticate": "Bearer"},            # --> HTTP başlıkları ile Bearer token gerektiğini belirtir
)


# Giriş için Token oluşturucu(JWT)
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()     # --> Token içine data kopyalanır, çünkü data üzerinde değişiklik yapılabilir
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15)) # --> istisna yoksa 15 dakika sonra token geçersiz olur
    to_encode.update({"exp": expire})  # --> Token'ın son kullanma tarihi payload'a ekler
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)   # --> Token'ı oluşturur ve döndürür


# Cookie'den token okuyarak kullanıcıyı döner
# try bloğunda dönen isteğe göre kullanıcının tokenini doğrular
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
# Token üzerinden "teacher" tipinde kullanıcıyı doğrular
def calendar_authentication_token(
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
        user_type: str = payload.get("user_type")
        if email is None or user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = create_calendar_by_auth(db, email, user_id, user_type=UserType.teacher)
    if user is None or user.type != UserType.teacher:
        raise credentials_exception
    return user

# Öğrenci yetkilendirme (cookie üzerinden)
# Token üzerinden "student" tipinde kullanıcıyı doğrular
def student_authentication_token(
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
        user_type: str = payload.get("user_type")
        if email is None or user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_student(db, email, user_id, user_type=UserType.student)
    if user is None or user.type != UserType.student:
        raise credentials_exception
    return user

# Admin yetkilendirme (cookie üzerinden)
# Token üzerinden "admin" tipinde kullanıcıyı doğrular
def admin_authentication_token(
    access_token: Optional[str] = Cookie(None),
    db: Session = Depends(get_db)
):
    if access_token is None:
        raise credentials_exception
    try:
        token = access_token.replace("Bearer ", "")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("username")
        email: str = payload.get("email")
        user_type: str = payload.get("user_type")
        if username is None or email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(LoginData).filter_by(username=username, email=email, type=UserType.admin).first()
    if user is None or user.type != UserType.admin:
        raise credentials_exception
    return user