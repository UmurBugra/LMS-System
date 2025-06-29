from sqlalchemy.orm import Session
from schemas import UserType, LoginBase
from db.models import LoginData

def create_setup_user(db: Session, request: LoginBase, user_type: UserType = "admin"):
    admin_setup = LoginData(
        username=request.username,
        password=request.password,
        email=request.email,
        type=user_type.value
    )
    db.add(admin_setup)
    db.commit()
    db.refresh(admin_setup)
    return admin_setup