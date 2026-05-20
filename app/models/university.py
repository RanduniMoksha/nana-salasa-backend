from sqlalchemy import Column, Integer, String
from app.database import Base

class University(Base):

    __tablename__ = "universities"

    university_id = Column(Integer, primary_key=True, index=True)

    university_name = Column(String(255), nullable=False)

    short_name = Column(String(50), nullable=False)

    location = Column(String(255), nullable=False)