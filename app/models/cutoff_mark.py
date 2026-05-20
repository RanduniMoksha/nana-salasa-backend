from sqlalchemy import Column, Integer, ForeignKey, DECIMAL
from app.database import Base

class CutoffMark(Base):

    __tablename__ = "cutoff_marks"

    cutoff_id = Column(Integer, primary_key=True, index=True)

    degree_id = Column(
        Integer,
        ForeignKey("degree_programs.degree_id")
    )

    district_id = Column(
        Integer,
        ForeignKey("districts.district_id")
    )

    year = Column(Integer)

    cutoff_zscore = Column(DECIMAL(4,3))