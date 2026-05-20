from pydantic import BaseModel


class UniversityResponse(BaseModel):

    university_id: int

    university_name: str

    class Config:
        from_attributes = True