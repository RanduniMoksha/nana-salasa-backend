from sqlalchemy import TIMESTAMP, Column, Integer, ForeignKey, DECIMAL
from app.database import Base
from sqlalchemy.sql import func

class StudentProfile(Base):

    __tablename__ = "student_profiles"

    student_id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.user_id"))

    stream_id = Column(Integer, ForeignKey("streams.stream_id"))

    district_id = Column(Integer, ForeignKey("districts.district_id"))

    z_score = Column(DECIMAL(4,3))

    al_year = Column(Integer)
    
    created_at = Column(TIMESTAMP, server_default=func.now())