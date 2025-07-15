from fastapi import Form, Body
from pydantic import BaseModel, EmailStr
from enum import Enum

# Kullanıcı türlerini tanımlayan Enum
class UserType(Enum):
    student = "student"
    teacher = "teacher"
    admin = "admin"

# Giriş ekranı için gerekli olan modeller
class LoginEmailPassword(BaseModel):
    email: EmailStr
    password: str

    # Bu şekilde obje kullanmak yerine var olan objeyi istediğimiz değeri atayıp kullanıyoruz
    @classmethod
    def form(
        cls,
        email: EmailStr = Form(...),
        password: str = Form(...)
    ):
        return cls(email=email, password=password)

# Kullanıcı giriş bilgilerini içeren model
class LoginBase(BaseModel):
    username: str
    password: str
    email: str

    @classmethod
    def form(
        cls,
        username: str = Form(...),
        email: str = Form(...),
        password: str = Form(...)
    ):
        return cls(username=username, email=email, password=password)

    @classmethod
    def body(
            cls,
            username: str = Body(...),
            email: str = Body(...),
            password: str = Body(...),
    ):
        return cls(username=username, email=email, password=password)


# Kullanıcı giriş bilgilerini içeren model
class LoginDisplay(BaseModel):
    username: str
    email: str
    type: str
    class Config:
        from_attributes = True

# Takvim günleri için Enum
class CalendarBase(Enum):
    Pazartesi = "Pazartesi"
    Salı = "Salı"
    Çarşamba = "Çarşamba"
    Perşembe = "Perşembe"
    Cuma = "Cuma"

# Takvim verilerini içeren model
class CalendarData(BaseModel):
    day: CalendarBase
    t_08_09: str
    t_09_10: str
    t_10_11: str
    t_11_12: str
    t_13_14: str
    t_14_15: str
    t_15_16: str
    t_16_17: str

class EventType(Enum):
    lecture = "lecture"
    lab = "lab"
    quiz = "quiz"
    exam = "exam"
    meeting = "meeting"

class EventStatus(Enum):
    planned = "planned"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"