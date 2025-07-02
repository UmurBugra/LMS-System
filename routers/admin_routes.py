from fastapi import APIRouter, Depends, Request ,Form, Body ,HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from db.database import get_db
from schemas import LoginBase, UserType, LoginDisplay
from crud import admin
from crud.notification import create_notification_for_all_students, create_notification_for_all_teachers
from authentication.oauth2 import admin_authentication_token


router = APIRouter(prefix="/admin-page", tags=["setup"])
templates = Jinja2Templates(directory="templates")

# Create user
@router.post("/create")
def create_user(
    form_data: LoginBase = Depends(LoginBase.form),
    type: UserType = Form(...),
    db: Session = Depends(get_db),
    create_user_by_auth: LoginBase = Depends(admin_authentication_token)
):
    user = admin.create_user_by_admin(db, form_data, type)
    return RedirectResponse("/nav/admin-home", status_code=302)

# Update user
@router.put("/update-user-{id}", response_model=LoginDisplay)
def update_user(
    id: int,
    body_data: LoginBase = Depends(LoginBase.body),
    type: UserType = Body(...),
    db: Session = Depends(get_db)
):

    if not body_data.username or not body_data.email or not body_data.password:
        raise HTTPException(status_code=400, detail="boş alanlar")

    return admin.update_user_by_admin(db, id, body_data, type)

# Delete user
@router.delete("/delete-user-{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    return admin.delete_user_by_admin(db, id)

# Create notification

@router.post("/create-notification")
def create_notification(
        content: str = Form(...),
        receiver: str = Form(None),
        db: Session = Depends(get_db),
        current_user: LoginBase = Depends(admin_authentication_token)
):
    if not content:
        raise HTTPException(status_code=400, detail="boş duyuru içeriği")
    try:

        if receiver == "all_students":
            create_notification_for_all_students(db, content, sender_username=current_user.username)
        elif receiver == "all_teachers":
           create_notification_for_all_teachers(db, content, sender_id=current_user.id)
        elif receiver == "everyone":
            admin.create_notification_for_everyone(db, content, sender_id=current_user.id)

        return JSONResponse({"message": "Duyuru başarıyla gönderildi."})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))