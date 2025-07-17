from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SQLAlchemyEnum
from db.database import Base
from models import notification_receivers
from schemas import UserType

class LoginData(Base):
    __tablename__ = "login_data"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    email = Column(String, unique=True, nullable=False)
    type =  Column(SQLAlchemyEnum(UserType)) # "student", "teacher"
    items = relationship("CalendarData", back_populates="user")
    created_courses = relationship("Course", back_populates="teacher")
    enrollments = relationship("Enrollment", back_populates="student")
    notifications = relationship("NotificationData",
        secondary=notification_receivers,
        back_populates="receiver"
    )