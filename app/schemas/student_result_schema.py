from pydantic import BaseModel
from typing import Optional


class StudentResultCreate(BaseModel):

    subject_id: int

    grade: str


class StudentResultResponse(BaseModel):

    result_id: int

    student_id: int

    subject_id: int

    grade: str

    class Config:
        from_attributes = True


class StudentResultUpdate(BaseModel):

    # Allow partial updates: student can update subject or grade (or both)
    subject_id: Optional[int] = None

    grade: Optional[str] = None