from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base


class RequirementGroup(Base):

    __tablename__ = "requirement_groups"

    group_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    template_id = Column(
        Integer,
        ForeignKey("requirement_templates.template_id"),
        nullable=False
    )

    group_name = Column(
        String(100),
        nullable=False
    )

    minimum_required = Column(
        Integer,
        nullable=False
    )