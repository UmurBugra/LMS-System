from fastapi import APIRouter, Depends, Query
from schemas import LoginDisplay, LoginBase
from crud import login, auth
from sqlalchemy.orm import Session
from db.database import get_db
from schemas import UserType
from authentication.oauth2 import create_user_authentication_token
router = APIRouter(prefix="/login", tags=["login"])

# Create user
@router.post("/", response_model=LoginDisplay)
def create_user(request: LoginBase, db: Session = Depends(get_db), type: UserType = Query(...),
                create_user_by_auth: LoginBase = Depends(create_user_authentication_token)):
    return login.create_user(db, request, type)

# Read all users
@router.get("/all", response_model=list[LoginDisplay])
def get_users(db: Session = Depends(get_db)):
    return login.get_read_user(db)

# Read user by id
@router.get("/{id}", response_model=LoginDisplay)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    return login.get_read_user_by_id(db, id)

# Update user
@router.put("/{id}", response_model=LoginDisplay)
def update_user(id: int, request: LoginBase, db: Session = Depends(get_db), type: UserType = Query(...)):
    return login.update_user(db, id, request, type)

# Delete user
@router.delete("/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    return login.delete_user(db, id)






