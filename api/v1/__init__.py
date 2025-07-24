from fastapi import APIRouter
from .endpoints import admin, login_auth, navigation, notification, oauth2, setup

api_router = APIRouter()

api_router.include_router(admin.router, prefix="/admin-page", tags=["admin"])
api_router.include_router(login_auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(navigation.router, prefix="/nav", tags=["navigation"])
api_router.include_router(notification.router, prefix="/notification", tags=["Notification"])
api_router.include_router(oauth2.router, tags=["authentication"])
api_router.include_router(setup.router, prefix="/setup", tags=["setup"])