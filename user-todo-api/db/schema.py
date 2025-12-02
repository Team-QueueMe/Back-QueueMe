from pydantic import BaseModel
from datetime import date, datetime
from typing import List, Optional, Literal


class TaskCreate(BaseModel):
    name: str
    description: Optional[str] = None
    priority: Literal['urgent', 'high', 'normal', 'low']
    category: Literal['meeting', 'study', 'event', 'etc']
    due_date: date


class TaskUpdateStatus(BaseModel):
    status: str 


class TaskResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    priority: str
    category: str
    due_date: date
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DailySummaryResponse(BaseModel):
    date: date
    progress_percentage: int
    tasks: List[TaskResponse]


class User(BaseModel):
    id: int
    email: str
    name: str | None = None
    class Config:
        from_attributes = True 

class Token(BaseModel):
    access_token: str
    token_type: str