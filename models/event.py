from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SQLAlchemyEnum
from db.database import Base
from schemas import CalendarBase

class CalendarData(Base):
    __tablename__ = "calendar_data"
    id = Column(Integer, primary_key=True, index=True)
    days = Column(SQLAlchemyEnum(CalendarBase), unique=False)
    t_08_09 = Column(String)
    t_09_10 = Column(String)
    t_10_11 = Column(String)
    t_11_12 = Column(String)
    t_13_14 = Column(String)
    t_14_15 = Column(String)
    t_15_16 = Column(String)
    t_16_17 = Column(String)
    user_id = Column(Integer, ForeignKey("login_data.id"))
    user = relationship("LoginData", back_populates="items")