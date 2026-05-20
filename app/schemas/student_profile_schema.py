from pydantic import BaseModel


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