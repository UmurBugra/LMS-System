from fastapi import HTTPException
from sqlalchemy.orm import Session
from schemas import LoginBase
from db.models import LoginData
from schemas import UserType

# CRUD operations for user login
# Create user
def create_user(db: Session, request: LoginBase, user_type: UserType):
    new_user = LoginData(
        username=request.username,
        password=request.password,
        email=request.email,
        type=user_type
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Create user with auth
def create_user_with_auth(db: Session, username: str, user_type: UserType):
    user = db.query(LoginData).filter(LoginData.username == username, LoginData.type == user_type).first()
    if not user:
        raise HTTPException(status_code=404, detail="Kullanıcı oluşturma öğretmen yetkisindedir.")
    return user

# Read all users
def get_read_user(db: Session):
    return db.query(LoginData).all()

# Read user by id
def get_read_user_by_id(db: Session, id: int):
    return db.query(LoginData).filter(LoginData.id == id).first()

# Update user
def update_user(db: Session, id: int, request: LoginBase, user_type: UserType):
    user = db.query(LoginData).filter(LoginData.id == id)
    user.update({
        "username": request.username,
        "password": request.password,
        "email": request.email,
        "type": user_type
    })
    db.commit()
    return user.first()

# Delete user
def delete_user(db: Session, id: int):
    user = db.query(LoginData).filter(LoginData.id == id).first()
    db.delete(user)
    db.commit()
    return "User deleted successfully"

def get_user_by_email_and_id(db: Session, email: str, user_id: int):
    user = db.query(LoginData).filter(LoginData.email == email, LoginData.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_user_student(db: Session, email: str, user_id: int, user_type: UserType):
    user = db.query(LoginData).filter(LoginData.email == email, LoginData.id == user_id, LoginData.type == user_type).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found or not a student")
    return user