from fastapi import FastAPI, Request
from routers import login_routes, login_auth_routes, calendar_routes, oauth2_routes
from db.database import engine
from db import models
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(login_routes.router)
app.include_router(login_auth_routes.router)
app.include_router(calendar_routes.router)
app.include_router(oauth2_routes.router)

@app.get("/")
def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

models.Base.metadata.create_all(bind=engine)