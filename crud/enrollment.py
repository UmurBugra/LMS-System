from sqlalchemy.orm import Session
from models import Enrollment

def create_enrollment(db: Session, course_id: int, student_id: int):

    try:
        existing_enrollment = db.query(Enrollment).filter(
            Enrollment.course_id == course_id,
            Enrollment.student_id == student_id
        ).first()

        if existing_enrollment:
            return None

    except Exception as e:
        print(e)

    new_enrollment = Enrollment(
        course_id=course_id,
        student_id=student_id
    )
    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)

    return new_enrollment

def delete_enrollment(db: Session, course_id: int, student_id: int):
    enrollment = db.query(Enrollment).filter(
        Enrollment.course_id == course_id,
        Enrollment.student_id == student_id
    ).first()

    if enrollment:
        db.delete(enrollment)
        db.commit()

    return enrollment