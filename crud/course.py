from sqlalchemy.orm import Session
from models import Course, Enrollment,LoginData

# Kurs oluşturma CRUD
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

# Kurs listeleme CRUD

def get_courses(db, student_id):

    get_c = db.query(Course, Enrollment).join(
        LoginData,
        LoginData.id == Enrollment.student_id
    ).filter(
        Course.id == Enrollment.course_id,
        Enrollment.student_id == student_id
    )

    courses = []

    for i in get_c:

        courses.append(i)

    return courses