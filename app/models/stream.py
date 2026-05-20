from sqlalchemy import Column, Integer, String
from app.database import Base

class Stream(Base):

    __tablename__ = "streams"

    stream_id = Column(Integer, primary_key=True, index=True)

    stream_name = Column(String(100), unique=True, nullable=False)