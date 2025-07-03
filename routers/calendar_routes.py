from fastapi import APIRouter, Depends, Request, Form, HTTPException
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates
from schemas import LoginBase, CalendarData, UserType
from crud.calendar import create_calendar, get_calendar, delete_calendar as delete_calendar_func
from db.database import get_db
from authentication.oauth2 import calendar_authentication_token, student_authentication_token
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/calendar", tags=["Calendar"])
templates = Jinja2Templates(directory="templates")


# GET: Takvim oluşturma formunu göster
@router.get("/create", response_class=HTMLResponse)
def show_create_calendar_form(
    request: Request,
    db: Session = Depends(get_db),
    current_user: LoginBase = Depends(calendar_authentication_token)
):
    # Kullanıcı tipini belirle
    if current_user.type == UserType.student:
        display_user_type = "Öğrenci"
    elif current_user.type == UserType.teacher:
        display_user_type = "Öğretmen"
    else:
        display_user_type = "Bilinmiyor"

    return templates.TemplateResponse(
        "create_calendar.html",
        {"request": request, "username": current_user.username, "user_type": display_user_type}
    )


# POST: Takvim oluşturma formu gönderildiğinde çalışır
@router.post("/create", response_class=HTMLResponse)
def handle_create_calendar(
    request: Request,
    days: str = Form(...),
    t_08_09: str = Form(...),
    t_09_10: str = Form(...),
    t_10_11: str = Form(...),
    t_11_12: str = Form(...),
    t_13_14: str = Form(...),
    t_14_15: str = Form(...),
    t_15_16: str = Form(...),
    t_16_17: str = Form(...),
    db: Session = Depends(get_db),
    current_user: LoginBase = Depends(calendar_authentication_token)
):
    # Kullanıcı tipini belirle
    if current_user.type == UserType.student:
        display_user_type = "Öğrenci"
    elif current_user.type == UserType.teacher:
        display_user_type = "Öğretmen"
    else:
        display_user_type = "Bilinmiyor"

    try:
        calendar_data = CalendarData(
            day=days,
            t_08_09=t_08_09,
            t_09_10=t_09_10,
            t_10_11=t_10_11,
            t_11_12=t_11_12,
            t_13_14=t_13_14,
            t_14_15=t_14_15,
            t_15_16=t_15_16,
            t_16_17=t_16_17
        )

        result = create_calendar(db, calendar_data, current_user)

        return templates.TemplateResponse(
            "create_calendar.html",
            {"request": request,
             "username": current_user.username,
             "user_type": display_user_type,
             "success_message": "Takvim başarıyla oluşturuldu.",
             "data": result
             }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "create_calendar.html",
            {"request": request,
             "username": current_user.username,
             "user_type": display_user_type,
             "error_message": f"Takvim oluşturulurken bir hata oluştu: {str(e)}"
             }
        )

# Takvim listeleme
@router.get("/teacher", response_class=HTMLResponse)
def show_teacher_calendar_list(request: Request,
                       db: Session = Depends(get_db),
                       current_user: LoginBase = Depends(calendar_authentication_token)
):
    # Kullanıcı tipini belirle
    if current_user.type == UserType.student:
        display_user_type = "Öğrenci"
    elif current_user.type == UserType.teacher:
        display_user_type = "Öğretmen"
    else:
        display_user_type = "Bilinmiyor"

    calendars = get_calendar(db)
    return templates.TemplateResponse(
        "teacher_calendars.html",
        {"request": request, "username": current_user.username, "user_type": display_user_type, "calendars": calendars}
    )

# Takvim silme işlemi
@router.post("/delete/{calendar_id}", response_class=HTMLResponse)
def delete_calendar(
    request: Request,
    calendar_id: int,
    db: Session = Depends(get_db),
    current_user: LoginBase = Depends(calendar_authentication_token)
):
    # Kullanıc�� tipini belirle
    if current_user.type == UserType.student:
        display_user_type = "Öğrenci"
    elif current_user.type == UserType.teacher:
        display_user_type = "Öğretmen"
    else:
        display_user_type = "Bilinmiyor"

    try:
        delete_calendar_func(db, calendar_id, current_user)
        calendars = get_calendar(db)                            # <-- Takvimleri yeniden al
        return templates.TemplateResponse(
            "teacher_calendars.html",
            {"request": request,
             "username": current_user.username,
             "user_type": display_user_type,
             "calendars": calendars,                            # <-- Güncellenmiş takvimleri kullanıcıya gönder
             "success_message": "Takvim başarıyla silindi"
             }
        )
    except HTTPException as e:
        calendars = get_calendar(db)
        return templates.TemplateResponse(
            "teacher_calendars.html",
            {"request": request,
             "username": current_user.username,
             "user_type": display_user_type,
             "calendars": calendars,
             "error_message": e.detail
             }
        )

# Öğrenci takvimi görüntüleme
@router.get("/student", response_class=HTMLResponse)
def show_student_calendar_list(
        request: Request,
        db: Session = Depends(get_db),
        current_user : LoginBase = Depends(student_authentication_token)
):
    # Kullanıcı tipini belirle
    if current_user.type == UserType.student:
        display_user_type = "Öğrenci"
    elif current_user.type == UserType.teacher:
        display_user_type = "Öğretmen"
    else:
        display_user_type = "Bilinmiyor"

    calendars = get_calendar(db)
    return templates.TemplateResponse(
        "student_calendars.html",
        {"request": request, "username": current_user.username, "user_type": display_user_type, "calendars": calendars}
    )