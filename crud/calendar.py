from sqlalchemy.orm import Session
from db.models import CalendarData, LoginData
from schemas import CalendarBase, Courses, UserType, LoginBase
from fastapi import HTTPException

# CRUD operations for Calendar

def create_calendar(db: Session, request: CalendarBase, course: Courses, current_user: LoginBase):
    username = current_user.username
    calendar_entry = CalendarData(
        days=request,
        t_08_09=course.t_08_09,
        t_09_10=course.t_09_10,
        t_10_11=course.t_10_11,
        t_11_12=course.t_11_12,
        t_13_14=course.t_13_14,
        t_14_15=course.t_14_15,
        t_15_16=course.t_15_16,
        t_16_17=course.t_16_17,
        user_name=username
    )
    db.add(calendar_entry)
    db.commit()
    db.refresh(calendar_entry)
    return calendar_entry

# token fonksiyonu
def create_calendar_by_auth(db: Session, username: str, user_type: UserType):
    user = db.query(LoginData).filter(LoginData.username == username, LoginData.type == user_type).first()
    if not user:
        raise HTTPException(status_code=404, detail="Takvim oluşturma sadece öğretmen yetkisindedir.")
    return user