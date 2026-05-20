from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.sql import func

from app.database import Base

class Recommendation(Base):

    __tablename__ = "recommendations"

    recommendation_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    student_id = Column(
        Integer,
        ForeignKey("student_profiles.student_id")
    )

    degree_id = Column(
        Integer,
        ForeignKey("degree_programs.degree_id")
    )

    recommendation_status = Column(String(20), nullable=False)

    generated_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )