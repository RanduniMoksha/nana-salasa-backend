from sqlalchemy import Column, ForeignKey, Integer, String
from app.database import Base

class DegreeStream(Base):

    __tablename__ = "degree_streams"

    id = Column(Integer, primary_key=True, index=True)

    degree_id = Column(Integer, ForeignKey("degree_programs.degree_id"))

    stream_id = Column(Integer, ForeignKey("streams.stream_id"))
