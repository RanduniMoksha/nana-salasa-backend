from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Faculty(Base):

    __tablename__ = "faculties"

    faculty_id = Column(Integer, primary_key=True, index=True)

    faculty_name = Column(String(255), nullable=False)

    university_id = Column(
        Integer,
        ForeignKey("universities.university_id")
    )
   