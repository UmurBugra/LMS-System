from pydantic import BaseModel
from enum import Enum

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