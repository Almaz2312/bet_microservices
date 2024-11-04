import enum
from pydantic import BaseModel
from datetime import datetime


class State(enum.Enum):
    NEW = 1
    FINISHED_WIN = 2
    FINISHED_LOSE = 3


class CreateBetSchema(BaseModel):
    event_id: int
    coefficient: float
    deadline: datetime
    state: State
