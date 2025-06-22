from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates
from schemas import CalendarBase, Courses, LoginBase, CalendarData
from crud.calendar import create_calendar
from db.database import get_db
from authentication.oauth2 import create_authentication_token
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/calendar", tags=["Calendar"])
templates = Jinja2Templates(directory="templates")


# GET: Takvim oluşturma formunu göster
@router.get("/create", response_class=HTMLResponse)
def show_create_calendar_form(
    request: Request,
    db: Session = Depends(get_db),
    current_user: LoginBase = Depends(create_authentication_token)
):
    return templates.TemplateResponse(
        "create_calendar.html",
        {"request": request, "username": current_user.username}
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
    current_user: LoginBase = Depends(create_authentication_token)
):
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
             "success_message": "Takvim başarıyla oluşturuldu.",
             "data": result
             }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "create_calendar.html",
            {"request": request,
             "username": current_user.username,
             "error_message": f"Takvim oluşturulurken bir hata oluştu: {str(e)}"
             }
        )