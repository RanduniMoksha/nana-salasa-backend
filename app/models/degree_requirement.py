from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base


class DegreeRequirement(Base):

    __tablename__ = "degree_requirements"

    degree_requirement_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    degree_id = Column(
        Integer,
        ForeignKey("degree_programs.degree_id"),
        nullable=False
    )

    template_id = Column(
        Integer,
        ForeignKey("requirement_templates.template_id"),
        nullable=False
    )