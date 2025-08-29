from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from db.database import get_db
from schemas import LoginBase
from authentication.oauth2 import get_current_user_from_token, teacher_authentication_token
from crud.course import create_course, get_courses
from crud.enrollment import create_enrollment, delete_enrollment
from schemas import UserType

router = APIRouter()
templates = Jinja2Templates(directory="templates")
security = HTTPBearer()

# Kurs oluşturma
@router.post("/create", dependencies=[Depends(security)])
def create_course_endpoint(
    name: str = Form(...),
    code: str = Form(...),
    description: str = Form(None),
    db: Session = Depends(get_db),
    current_user: LoginBase = Depends(teacher_authentication_token)
):
    if current_user.type != UserType.teacher:
        raise HTTPException(status_code=403, detail="Only teachers can create courses")

    return create_course(db, name, code, description, current_user)

# Kurs kaydı yapma
@router.post("/{course_id}/enroll", dependencies=[Depends(security)])
def enroll_in_course(
    course_id: int,
    student_id: int = Form(...),
    db: Session = Depends(get_db),
    current_user: LoginBase = Depends(teacher_authentication_token)
):
    if current_user.type != UserType.teacher:
        raise HTTPException(status_code=403, detail="Only teachers can enroll students")

    enrollment = create_enrollment(db, course_id, student_id)
    return enrollment

# Kurs kaydı silme
@router.delete("/{course_id}/unenroll", dependencies=[Depends(security)])
def unenroll_from_course(
    course_id: int,
    student_id: int = Form(...),
    db: Session = Depends(get_db),
    current_user: LoginBase = Depends(teacher_authentication_token)
):
    if current_user.type != UserType.teacher:
        raise HTTPException(status_code=403, detail="Only teachers can remove students from courses")

    enrollment = delete_enrollment(db, course_id, student_id)
    return enrollment

# Kurs listeleme
@router.get("/", dependencies=[Depends(security)])
def get_course(
        db: Session = Depends(get_db),
        current_user: LoginBase = Depends(get_current_user_from_token),
):

    courses = get_courses(db, current_user.username, current_user.id)
    return courses