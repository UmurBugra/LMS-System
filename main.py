from fastapi import FastAPI, Request, Depends
from db.database import engine, get_db
from models import LoginData
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from authentication.oauth2 import TokenExpiredException
import models
from api.v1 import api_router as router

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates") # Jinja2 şablonları için dizin

app.include_router(router, prefix="/api/v1")

# Veritabanında admin kullanıcının olup olmadığını kontrol eden fonksiyon
def is_admin_user(db):
    admin = db.query(LoginData).filter(LoginData.type == "admin").first()
    return admin

# Ana sayfa rotası
@app.get("/")
def root(request: Request, db: Session = Depends(get_db)):
    if not is_admin_user(db):
        return templates.TemplateResponse("setup.html", {"request": request})
    else:
        return templates.TemplateResponse("index.html", {"request": request}) # şablonu render eder

models.Base.metadata.create_all(bind=engine)

# Token süresi dolduğunda exception handler
@app.exception_handler(TokenExpiredException) # Eğer TokenExpiredException oluşursa bu handler devreye girer
def token_expired_exception_handler(request: Request, exc: TokenExpiredException):
    response = templates.TemplateResponse(
        "index.html",
        {"request": request, "error": exc.message}
    )
    # Cookie temizleme
    response.delete_cookie("access_token")
    return response