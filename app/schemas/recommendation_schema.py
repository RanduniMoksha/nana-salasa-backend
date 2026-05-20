from pydantic import BaseModel
from datetime import datetime


class RecommendationResponse(BaseModel):

    recommendation_id: int

    student_id: int

    degree_id: int

    created_at: datetime

    class Config:
        from_attributes = True