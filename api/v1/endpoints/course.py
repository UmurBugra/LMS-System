from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from db.database import get_db
from schemas import LoginBase
from authentication.oauth2 import get_current_user_from_cookie
from crud.course import create_course
from crud.enrollment import create_enrollment, delete_enrollment

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post("create")
def create_course_endpoint(
    name: str = Form(...),
    code: str = Form(...),
    description: str = Form(None),
    db: Session = Depends(get_db),
    current_user: LoginBase = Depends(get_current_user_from_cookie)
):
    return create_course(db, name, code, description, current_user)

@router.post("{course_id}/enroll")
def enroll_in_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: LoginBase = Depends(get_current_user_from_cookie)
):

    enrollment = create_enrollment(db, course_id, current_user.id)

    return enrollment

@router.delete("{course_id}/unenroll")
def unenroll_from_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: LoginBase = Depends(get_current_user_from_cookie)
):
    enrollment = delete_enrollment(db, course_id, current_user.id)

    return enrollment