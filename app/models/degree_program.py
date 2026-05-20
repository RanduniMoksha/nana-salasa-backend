from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class DegreeProgram(Base):

    __tablename__ = "degree_programs"

    degree_id = Column(Integer, primary_key=True, index=True)

    degree_name = Column(String(255), nullable=False)

    university_id = Column(
        Integer,
        ForeignKey("universities.university_id")
    )

    faculty_id = Column(
        Integer,
        ForeignKey("faculties.faculty_id")
    )

    stream_id = Column(
        Integer,
        ForeignKey("streams.stream_id")
    )

    duration_years = Column(Integer, nullable=False)

    description = Column(String(1000), nullable=True)