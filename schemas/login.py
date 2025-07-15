from pydantic import BaseModel, EmailStr
from fastapi import Form
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