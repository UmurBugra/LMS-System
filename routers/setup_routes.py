from fastapi import APIRouter, Depends, Form, Request
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
        request: Request,
        username: str = Form(...),
        password: str = Form(...),
        email: str = Form(...),
        db: Session = Depends(get_db)
):
    user = LoginBase(username=username, password=password, email=email)
    setup_user = setup.create_setup_user(db, user, user_type=UserType.admin)
    return templates.TemplateResponse(
        "index.html", {
            "request": request,
            "message": "Admin user created successfully.",
            "user": setup_user,
            "user_type": UserType.admin
        }
    )