from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base

class UniversityFaculty(Base):
    __tablename__ = "university_faculties"

    university_faculty_id = Column(Integer, primary_key=True, index=True)

    university_id = Column(
        Integer,
        ForeignKey("universities.university_id"),
        nullable=False
    )

    faculty_id = Column(
    Integer,
    ForeignKey("faculties.faculty_id"),
    nullable=False
)