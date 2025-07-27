from sqlalchemy.orm import Session
from models import Course, Enrollment, LoginData
from schemas import UserType

def create_course(db: Session, name: str, code: str, description: str, current_user):

    new_course = Course(
        name=name,
        code=code,
        description=description,
        teacher_id=current_user.id
    )
    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return new_course