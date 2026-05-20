from pydantic import BaseModel


class FacultiesResponse(BaseModel):

    faculty_id: int

    faculty_name: str

    class Config:
        from_attributes = True