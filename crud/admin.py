from sqlalchemy.orm import Session
from schemas import UserType, LoginBase
from db.models import LoginData

#CRUD operations for admin
# Create user
def create_user_by_admin(db: Session, request, user_type: UserType):
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

# Read all users
def get_read_users_by_admin(db: Session):
    return db.query(LoginData).all()

# Read user by id
def read_user_by_admin(db: Session, id: int):
    return db.query(LoginData).filter(LoginData.id == id).first()

# Update user
def update_user_by_admin(db: Session, id: int, request: LoginBase, user_type: UserType):
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
def delete_user_by_admin(db: Session, id: int):
    user = db.query(LoginData).filter(LoginData.id == id).first()
    db.delete(user)
    db.commit()
    return "User deleted successfully"