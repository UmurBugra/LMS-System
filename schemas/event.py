from pydantic import BaseModel
from enum import Enum

class CalendarBase(Enum):
    Pazartesi = "Pazartesi"
    Salı = "Salı"
    Çarşamba = "Çarşamba"
    Perşembe = "Perşembe"
    Cuma = "Cuma"

# Takvim verilerini içeren model
class CalendarData(BaseModel):
    day: CalendarBase
    t_08_09: str
    t_09_10: str
    t_10_11: str
    t_11_12: str
    t_13_14: str
    t_14_15: str
    t_15_16: str
    t_16_17: str

class EventType(Enum):
    lecture = "lecture"
    lab = "lab"
    quiz = "quiz"
    exam = "exam"
    meeting = "meeting"

class EventStatus(Enum):
    planned = "planned"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"