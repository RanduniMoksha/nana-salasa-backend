from pydantic import BaseModel
from typing import Optional


class StudentProfileCreate(BaseModel):

    stream_id: int

    district_id: int

    z_score: float

    al_year: int


class StudentProfileResponse(BaseModel):

    student_id: int

    user_id: int

    stream_id: int

    district_id: int

    z_score: float

    al_year: int

    class Config:
        from_attributes = True


class StudentProfileUpdate(BaseModel):

    # All fields are optional for partial updates. Provide only the fields
    # the student wants to change.
    stream_id: Optional[int] = None

    district_id: Optional[int] = None

    z_score: Optional[float] = None

    al_year: Optional[int] = None