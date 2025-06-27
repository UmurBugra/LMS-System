from pydantic import BaseModel, EmailStr
from enum import Enum

class UserType(Enum):
    student = "student"
    teacher = "teacher"

# Giriş ekranı için gerekli olan modeller
class LoginEmailPassword(BaseModel):
    email: EmailStr
    password: str

class LoginBase(BaseModel):
    username: str
    password: str
    email: str

class LoginDisplay(BaseModel):
    username: str
    email: str
    type: str
    class Config:
        from_attributes = True

class AuthUserType(BaseModel):
    username: str
    email: str

# Calander
class CalendarBase(Enum):
    Pazartesi = "Pazartesi"
    Salı = "Salı"
    Çarşamba = "Çarşamba"
    Perşembe = "Perşembe"
    Cuma = "Cuma"

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

class Courses(BaseModel):
    t_08_09: str
    t_09_10: str
    t_10_11: str
    t_11_12: str
    t_13_14: str
    t_14_15: str
    t_15_16: str
    t_16_17: str
