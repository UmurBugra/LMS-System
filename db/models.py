from db.database import Base
from sqlalchemy.sql.sqltypes import Integer, String, Boolean
from sqlalchemy import Column, DateTime, func, Table
from sqlalchemy import Enum as SQLAlchemyEnum
from schemas import UserType, CalendarBase
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

notification_receivers = Table(
    "notification_receivers",
    Base.metadata,
    Column("notification_id", Integer, ForeignKey("notification_data.id")),
    Column("user_name", String, ForeignKey("login_data.username")),
    Column("is_removed", Boolean, default=False, nullable=False)
)

# Kullanıcı bilgileri
class LoginData(Base):
    __tablename__ = "login_data"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)
    type =  Column(SQLAlchemyEnum(UserType)) # "student", "teacher"
    items = relationship("CalendarData", back_populates="user")
    notifications = relationship("NotificationData", secondary=notification_receivers, back_populates="receiver")

# Takvim verileri
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
    user_name = Column(String, ForeignKey("login_data.username"))
    user = relationship("LoginData", back_populates="items")

class NotificationData(Base):
    __tablename__ = "notification_data"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    created_time = Column(DateTime(timezone=True), default=func.now())
    sender_username = Column(String, ForeignKey("login_data.username"))
    # Birden fazla ilişki olabilir, bu yüzden foreign_keys ile belirtiliyor
    sender = relationship("LoginData", foreign_keys=[sender_username])
    # many-to-many relationship LoginData
    receiver = relationship("LoginData", secondary=notification_receivers, back_populates="notifications")