from sqlalchemy import Column, Integer, String
from app.database import Base


class RequirementTemplate(Base):

    __tablename__ = "requirement_templates"

    template_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    template_name = Column(
        String(100),
        nullable=False
    )