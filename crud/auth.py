from sqlalchemy.orm import Session
from schemas import LoginBase, AuthUserType, UserType
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
def user_login(db: Session, request: LoginBase, user_type: UserType):
    user = db.query(LoginData).filter(
        LoginData.username == request.username, LoginData.password == request.password, LoginData.email == request.email,
    LoginData.type == user_type).first()
    if not user:
        return "Hatalı giriş bilgileri. Lütfen tekrar deneyin."
    else:
        return "Giriş yapıldı"
