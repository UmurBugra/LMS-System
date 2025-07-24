from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from db.database import Base


class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    # Oluşturulan öğretmen
    teacher_id = Column(Integer, ForeignKey("login_data.id"), nullable=False)

    # Relationships
    teacher = relationship("LoginData", back_populates="created_courses")
    event = relationship("Event", back_populates="course")
    enrollments = relationship("Enrollment", back_populates="course")
