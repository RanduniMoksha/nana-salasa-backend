from pydantic import BaseModel


class DegreeProgramResponse(BaseModel):

    degree_id: int

    degree_name: str

    university_id: int

    class Config:
        from_attributes = True