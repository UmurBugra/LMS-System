from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.database import Base

notification_receivers = Table(
    "notification_receivers",
    Base.metadata,
Column("user_id", Integer, ForeignKey("login_data.id"), primary_key=True),
    Column("notification_id", Integer, ForeignKey("notification_data.id"), primary_key=True),
    Column("is_read", Boolean, default=False, nullable=False),
    Column("is_removed", Boolean, default=False, nullable=False),
    Column("is_removed_time", DateTime, nullable=True)
)

class NotificationData(Base):
    __tablename__ = "notification_data"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    created_time = Column(DateTime(timezone=True), default=func.now())
    sender_id = Column(Integer, ForeignKey("login_data.id"))
    # Birden fazla ilişki olabilir, bu yüzden foreign_keys ile belirtiliyor
    sender = relationship("LoginData", foreign_keys=[sender_id])
    redirect_url = Column(String, nullable=True)
    # many-to-many relationship LoginData
    receiver = relationship(
        "LoginData",
        secondary=notification_receivers,
        back_populates="notifications",
    )