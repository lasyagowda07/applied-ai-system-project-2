from typing import List, Optional
from pydantic import BaseModel


class TextRequest(BaseModel):
    text: str


class TaskResponse(BaseModel):
    pet_name: str
    species: str = "unknown"
    description: str
    task_type: str
    time: Optional[str] = None
    recurrence: Optional[str] = None
    priority: int = 1
    completed: bool = False


class ScheduleResponse(BaseModel):
    owner: str
    pets: List[dict]
    schedule: List[dict]
    conflicts: List[dict]
    confidence: float
    warnings: List[str]
    agent_steps: List[str]


class ValidationResponse(BaseModel):
    is_valid: bool
    warnings: List[str]
    missing_fields: List[str]
    confidence: float