from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base

class StreamSubject(Base):

    __tablename__ = "stream_subjects"

    stream_subject_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    stream_id = Column(
        Integer,
        ForeignKey("streams.stream_id")
    )

    subject_id = Column(
        Integer,
        ForeignKey("subjects.subject_id")
    )