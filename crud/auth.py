from sqlalchemy.orm import Session
from schemas import LoginEmailPassword
from models import LoginData

# CRUD operations for user authentication
# User Login Control
def user_login(db: Session, request: LoginEmailPassword): # Parametreler güncellendi
    user = db.query(LoginData).filter(LoginData.email == request.email).first()
    if not user:
        return "Hatalı giriş bilgileri. Lütfen tekrar deneyin."

    if user.password != request.password:
        return "Hatalı giriş bilgileri. Lütfen tekrar deneyin."
    return {
        "message": "Giriş yapıldı",
        "username": user.username,
        "email": user.email,
        "user_type": user.type.value, # Veritabanından kullanıcı tipini al
        "id": user.id
        }