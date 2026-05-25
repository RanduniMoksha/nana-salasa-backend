from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal

from app.models.degree_program import DegreeProgram
from app.models.faculty import Faculty
from app.models.university import University
# UniversityFaculty is not needed; DegreeProgram has university_id

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.get("/degrees")
def search_degrees(
    search: str = "",
    university_id: int = None,
    faculty_id: int = None,
    db: Session = Depends(get_db)
):

    query = db.query(
        DegreeProgram,
        Faculty,
        University
    ).join(
        Faculty,
        DegreeProgram.faculty_id == Faculty.faculty_id
    ).join(
        University,
        DegreeProgram.university_id == University.university_id
    )

    if search:
        query = query.filter(
            DegreeProgram.degree_name.ilike(f"%{search}%")
        )

    if university_id:
        query = query.filter(
            University.university_id == university_id
        )

    if faculty_id:
        query = query.filter(
            Faculty.faculty_id == faculty_id
        )

    results = query.all()

    response = []

    for degree, faculty, university in results:
        response.append({
            "degree_id": degree.degree_id,
            "degree_name": degree.degree_name,
            "faculty_name": faculty.faculty_name,
            "university_name": university.university_name
        })

    return response