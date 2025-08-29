from fastapi import Depends, Cookie, HTTPException, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer
from jose import jwt, JWTError
from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from db.database import get_db
from models import LoginData
from crud.login import get_user_by_email_and_id, get_user_student
from schemas import UserType

SECRET_KEY = 'd68209ffa66480a47408acdc06f3d35016a7e3dfbbec769592ccd9e56d97ba7e'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Bearer token scheme for Swagger UI
security = HTTPBearer()

# OAuth2 password bearer for automatic Swagger UI integration
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")

# Token süresi dolduğunda özel exception sınıfı
class TokenExpiredException(Exception):
    def __init__(self, message: str = "Oturum süresi doldu, lütfen tekrar giriş yapın."):
        self.message = message
        super().__init__(self.message) # --> Miras alınan sınıfın init metodunu çağırır ve ona hata mesajını iletir
        # super kullanmazsak "except TokenExpiredExceptionNoSuper as e" {e.message} şeklinde hata mesajını almamız gerekir

# Giriş için Token oluşturucu(JWT)
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()     # --> Token içine data kopyalanır, çünkü data üzerinde değişiklik yapılabilir
    if expires_delta:           # --> Eğer expires_delta belirtilmişse
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})  # --> Token'ın son kullanma tarihi payload'a ekler
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)   # --> Token'ı oluşturur ve döndürür

# Token'ı doğrula ve payload döndür
def verify_token(token: str):
    try:
        if token.startswith("Bearer "):
            token = token.replace("Bearer ", "")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise TokenExpiredException("Geçersiz token")

# Token'ı hem Bearer hem Cookie'den al
def get_token_from_request(
    authorization: Optional[str] = Header(None),
    access_token: Optional[str] = Cookie(None)
) -> str:
    # Önce Authorization header'ı kontrol et (Swagger UI için)
    if authorization and authorization.startswith("Bearer "):
        return authorization

    # Sonra cookie'yi kontrol et (Web UI için)
    if access_token and access_token.startswith("Bearer "):
        return access_token

    raise TokenExpiredException("Token bulunamadı")

# Cookie'den veya Bearer token'dan kullanıcıyı döner
def get_current_user_from_token(
    token: str = Depends(get_token_from_request),
    db: Session = Depends(get_db)
):
    payload = verify_token(token)
    email: str = payload.get("sub")
    user_id: int = payload.get("user_id")

    if email is None or user_id is None:
        raise TokenExpiredException("Token'da gerekli bilgiler eksik")

    user = get_user_by_email_and_id(db, email, user_id)
    if user is None:
        raise TokenExpiredException("Kullanıcı bulunamadı")
    return user

# Eski fonksiyon için backward compatibility
def get_current_user_from_cookie(
    access_token: Optional[str] = Cookie(None),
    db: Session = Depends(get_db)
):
    if access_token is None:
        raise TokenExpiredException()

    payload = verify_token(access_token)
    email: str = payload.get("sub")
    user_id: int = payload.get("user_id")

    if email is None or user_id is None:
        raise TokenExpiredException()

    user = get_user_by_email_and_id(db, email, user_id)
    if user is None:
        raise TokenExpiredException()
    return user

# Öğrenci yetkilendirme
def student_authentication_token(
    token: str = Depends(get_token_from_request),
    db: Session = Depends(get_db)
):
    payload = verify_token(token)
    email: str = payload.get("sub")
    user_id: int = payload.get("user_id")
    user_type: str = payload.get("user_type")

    if email is None or user_id is None:
        raise TokenExpiredException("Token'da gerekli bilgiler eksik")

    user = get_user_student(db, email, user_id, user_type=UserType.student)
    if user is None or user.type != UserType.student:
        raise TokenExpiredException("Yetkisiz erişim - Öğrenci girişi gerekli")
    return user

# Öğretmen yetkilendirme
def teacher_authentication_token(
    token: str = Depends(get_token_from_request),
    db: Session = Depends(get_db)
):
    payload = verify_token(token)
    email: str = payload.get("sub")
    user_id: int = payload.get("user_id")
    user_type: str = payload.get("user_type")

    if email is None or user_id is None:
        raise TokenExpiredException("Token'da gerekli bilgiler eksik")

    user = db.query(LoginData).filter_by(email=email, id=user_id, type=UserType.teacher).first()
    if user is None or user.type != UserType.teacher:
        raise TokenExpiredException("Yetkisiz erişim - Öğretmen girişi gerekli")
    return user

# Admin yetkilendirme
def admin_authentication_token(
    token: str = Depends(get_token_from_request),
    db: Session = Depends(get_db)
):
    payload = verify_token(token)
    username = payload.get("username")
    email: str = payload.get("sub")
    user_type: str = payload.get("user_type")
    user_id: int = payload.get("user_id")

    if username is None or email is None or user_id is None:
        raise TokenExpiredException("Token'da gerekli bilgiler eksik")

    user = db.query(LoginData).filter_by(username=username, email=email, id=user_id, type=UserType.admin).first()
    if user is None or user.type != UserType.admin:
        raise TokenExpiredException("Yetkisiz erişim - Admin girişi gerekli")
    return user