from fastapi import FastAPI
from routers import login_routes, login_auth_routes, calendar_routes, oauth2_routes
from db.database import engine
from db import models
app = FastAPI()
app.include_router(login_routes.router)
app.include_router(login_auth_routes.router)
app.include_router(calendar_routes.router)
app.include_router(oauth2_routes.router)
@app.get("/")
def root():
    return {"message": "Hello World"}

models.Base.metadata.create_all(bind=engine)

# Models kısmını foreign key ile güncelledim. Önce test et