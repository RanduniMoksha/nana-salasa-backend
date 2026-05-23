from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base


class GroupSubject(Base):

    __tablename__ = "group_subjects"

    group_subject_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    group_id = Column(
        Integer,
        ForeignKey("requirement_groups.group_id"),
        nullable=False
    )

    subject_id = Column(
        Integer,
        ForeignKey("subjects.subject_id"),
        nullable=False
    )

    required_grade = Column(
        String(2),
        nullable=False
    )