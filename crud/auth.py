from sqlalchemy.orm import Session
from schemas import LoginBase, AuthUserType, UserType, LoginEmailPassword
from db.models import LoginData
from fastapi import HTTPException, status

# CRUD operations for user authentication

# User student or teacher
def user_type_request(db: Session, request: AuthUserType):
    user = db.query(LoginData).filter(
        LoginData.username == request.username, LoginData.email == request.email).first()

    if not user:
        return "User not found"

    user_type = user.type.value
    if user_type == "student":
        return "Öğrenci"
    elif user_type == "teacher":
        return "Öğretmen"
    else:
        return "Unknown user type"

# User Login Control
def user_login(db: Session, request: LoginEmailPassword): # Parametreler güncellendi
    user = db.query(LoginData).filter(LoginData.email == request.email).first()
    if not user:
        return "Hatalı giriş bilgileri. Lütfen tekrar deneyin."

    if user.password != request.password:
        return "Hatalı giriş bilgileri. Lütfen tekrar deneyin."
        # Başarılı giriş durumunda kullanıcı bilgilerini döndür
    return {
        "message": "Giriş yapıldı",
        "username": user.username,
        "email": user.email,
        "user_type": user.type.value # Veritabanından kullanıcı tipini al
        }
