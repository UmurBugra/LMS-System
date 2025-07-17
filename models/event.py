from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SQLAlchemyEnum
from db.database import Base
from schemas import EventType, EventStatus


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)
    location = Column(String, nullable=True)    # --> amfi veya online
    event_type = Column(SQLAlchemyEnum(EventType))
    event_status = Column(SQLAlchemyEnum(EventStatus))
    # kurs kime ait
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    course = relationship("Course", back_populates="event")