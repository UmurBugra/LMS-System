from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import CalendarBase, Courses, LoginBase
from crud.calendar import create_calendar
from db.database import get_db
from authentication.oauth2 import create_authentication_token

router = APIRouter(prefix="/calendar", tags=["Calendar"])

# Create a new calendar entry
@router.post("/")
def handle_create_calendar(request: CalendarBase, course: Courses, db: Session = Depends(get_db),
                           create_auth: LoginBase = Depends(create_authentication_token)):
    return {
        "data": create_calendar(db, request, course),
        "current_user": create_auth
    }