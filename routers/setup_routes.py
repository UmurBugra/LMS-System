from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from db.database import get_db
from crud import setup
from schemas import LoginBase,UserType

router = APIRouter(prefix="/setup", tags=["setup"])
templates = Jinja2Templates(directory="templates")

# Initial setup route
@router.post("/")
def create_setup(
        username: str = Form(...),
        password: str = Form(...),
        email: str = Form(...),
        db: Session = Depends(get_db)
):
    request = LoginBase(username=username, password=password, email=email)
    return setup.create_setup_user(db, request, user_type=UserType.admin)