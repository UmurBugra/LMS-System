from fastapi import Form, Body
from pydantic import BaseModel
from enum import Enum

# Kullanıcı türlerini tanımlayan Enum
class UserType(Enum):
    student = "student"
    teacher = "teacher"
    admin = "admin"

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