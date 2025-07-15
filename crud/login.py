from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import LoginData
from schemas import UserType


# Kullanıcıyı email ve id ile veritabanından alır
def get_user_by_email_and_id(db: Session, email: str, user_id: int):
    user = db.query(LoginData).filter(LoginData.email == email, LoginData.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Kullanıcının öğrenci olup olmadığını kontrol eder ve kullanıcıyı getirir
def get_user_student(db: Session, email: str, user_id: int, user_type: UserType):
    user = db.query(LoginData).filter(LoginData.email == email, LoginData.id == user_id, LoginData.type == user_type).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found or not a student")
    return user