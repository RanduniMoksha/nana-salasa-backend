from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import SessionLocal

from app.models.degree_program import DegreeProgram
from app.models.faculty import Faculty
from app.models.university import University
# UniversityFaculty is not needed; DegreeProgram has university_id
from app.models.faculty import Faculty
from app.models.degree_program import DegreeProgram
from app.services.eligibility_service import find_degrees_by_subjects

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


@router.get("/degrees-by-subjects")
def degrees_by_subjects(
        subjects: List[int] = Query(..., description="List of subject IDs to search by (provide at least one)."),
        db: Session = Depends(get_db)
):
        """
        Search degree programs by a list of subject IDs.

        Behaviour:
        - The endpoint accepts one-or-more `subjects` query parameters (e.g.
            `/degrees-by-subjects?subjects=1&subjects=2&subjects=3`).
        - It returns degrees whose requirement templates reference ALL provided subjects.
        - This is a simple inclusion-based match. Commented and straightforward so you
            can adapt it later to use grade checks or minimum-group logic.
        """

        # call the service that encapsulates the matching logic
        matched_degrees = find_degrees_by_subjects(db, subjects)

        response = []

        for degree in matched_degrees:
                # fetch faculty and university names for friendly output
                faculty = db.query(Faculty).filter(Faculty.faculty_id == degree.faculty_id).first()
                university = db.query(University).filter(University.university_id == degree.university_id).first()

                response.append({
                        "degree_id": degree.degree_id,
                        "degree_name": degree.degree_name,
                        "faculty_name": faculty.faculty_name if faculty else None,
                        "university_name": university.university_name if university else None
                })

        return response