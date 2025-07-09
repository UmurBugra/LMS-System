from fastapi import FastAPI, Request, Depends
from routers import login_auth_routes, calendar_routes, oauth2_routes, navigation_routes, \
notification_routes, setup_routes, admin_routes
from db.database import engine, get_db
from db import models
from db.models import LoginData
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="/home/ubuntu/LMS-System/templates") # Jinja2 şablonları için dizin

app.include_router(login_auth_routes.router)
app.include_router(calendar_routes.router)
app.include_router(oauth2_routes.router)
app.include_router(navigation_routes.router)
app.include_router(notification_routes.router)
app.include_router(setup_routes.router)
app.include_router(admin_routes.router)

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