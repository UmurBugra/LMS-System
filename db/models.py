from db.database import Base
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy import Column
from sqlalchemy import Enum as SQLAlchemyEnum
from schemas import UserType, CalendarBase
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

class LoginData(Base):
    __tablename__ = "login_data"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)
    type =  Column(SQLAlchemyEnum(UserType)) # "student", "teacher"
    items = relationship("CalendarData", back_populates="user")

class CalendarData(Base):
    __tablename__ = "calendar_data"
    id = Column(Integer, primary_key=True, index=True)
    days = Column(SQLAlchemyEnum(CalendarBase), unique=True)
    t_08_09 = Column(String)
    t_09_10 = Column(String)
    t_10_11 = Column(String)
    t_11_12 = Column(String)
    t_13_14 = Column(String)
    t_14_15 = Column(String)
    t_15_16 = Column(String)
    t_16_17 = Column(String)
    user_name = Column(String, ForeignKey("login_data.username"))
    user = relationship("LoginData", back_populates="items")

