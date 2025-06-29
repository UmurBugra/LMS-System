from fastapi import APIRouter, Depends, Query, Form
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from db.database import get_db
from schemas import LoginBase,UserType
from crud import admin
from authentication.oauth2 import create_user_authentication_token, admin_authentication_token
from schemas import LoginDisplay

router = APIRouter(prefix="/admin-page", tags=["setup"])
templates = Jinja2Templates(directory="templates")

@router.post("/create", response_model=LoginDisplay)
def create_user(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    type: UserType = Form(...),
    db: Session = Depends(get_db),
    create_user_by_auth: LoginBase = Depends(admin_authentication_token)
):
    request = LoginBase(username=username, email=email, password=password)
    return admin.create_user_by_admin(db, request, type)

# Read all users
@router.get("/get-user-all", response_model=list[LoginDisplay])
def get_users(db: Session = Depends(get_db)):
    return admin.get_read_users_by_admin(db)

# Read user by id
@router.get("/get-user-by-{id}", response_model=LoginDisplay)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    return admin.read_user_by_admin(db, id)

# Update user
@router.put("/update-user-{id}", response_model=LoginDisplay)
def update_user(id: int, request: LoginBase, db: Session = Depends(get_db), type: UserType = Query(...)):
    return admin.update_user_by_admin(db, id, request, type)

# Delete user
@router.delete("/delete-user-{id}")
def delete_user(id: int, db: Session = Depends(get_db), delete_user_by_auth: LoginBase = Depends(create_user_authentication_token)):
    return admin.delete_user_by_admin(db, id)
