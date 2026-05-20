from pydantic import BaseModel


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