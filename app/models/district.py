from sqlalchemy import Column, Integer, String
from app.database import Base

class District(Base):

    __tablename__ = "districts"

    district_id = Column(Integer, primary_key=True, index=True)

    district_name = Column(String(100), nullable=False)