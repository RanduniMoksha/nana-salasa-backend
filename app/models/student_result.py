from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class StudentResult(Base):

    __tablename__ = "student_results"

    result_id = Column(Integer, primary_key=True, index=True)

    Student_id = Column(
        Integer,
        ForeignKey("student_profiles.student_id")
    )

    subject_id = Column(
        Integer,
        ForeignKey("subjects.subject_id")
    )

    grade = Column(String(2), nullable=False)