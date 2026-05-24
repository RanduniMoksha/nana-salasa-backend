from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class DegreeProgram(Base):

    __tablename__ = "degree_programs"

    degree_id = Column(Integer, primary_key=True, index=True)

    uni_code = Column(String(10), nullable=False)

    degree_name = Column(String(255), nullable=False)

    short_name = Column(String(50), nullable=True)

    university_id = Column(
        Integer,
        ForeignKey("universities.university_id")
    )

    duration_years = Column(Integer, nullable=False)

    intake = Column(Integer, nullable=False)

    medium = Column(String(50), nullable=False)

    description = Column(String(1000), nullable=True)

    faculty_id = Column(
    Integer,
    ForeignKey("faculties.faculty_id"),
    nullable=False
)

    requires_aptitude_test = Column(Integer, nullable=False)  # 0 or 1