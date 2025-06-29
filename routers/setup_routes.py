from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from db.database import get_db
from crud import setup
from schemas import LoginBase

router = APIRouter(prefix="/setup", tags=["setup"])
templates = Jinja2Templates(directory="templates")

@router.post("/")
def create_setup(request: LoginBase, db: Session = Depends(get_db)):
    return setup.create_setup_user(db, request)