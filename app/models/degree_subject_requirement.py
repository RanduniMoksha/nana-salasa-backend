from sqlalchemy import Column, Integer, ForeignKey, String
from app.database import Base

class DegreeSubjectRequirement(Base):

    __tablename__ = "degree_subject_requirements"

    requirement_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    degree_id = Column(
        Integer,
        ForeignKey("degree_programs.degree_id")
    )

    subject_id = Column(
        Integer,
        ForeignKey("subjects.subject_id")
    )

    required_grade = Column(String(2), nullable=False)