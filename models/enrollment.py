from sqlalchemy import Column, Integer
from sqlalchemy import ForeignKey
from db.database import Base
from sqlalchemy.orm import relationship

class Enrollment(Base):
    __tablename__ = "enrollments"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("login_data.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)

    # Relationships
    student = relationship("LoginData", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")