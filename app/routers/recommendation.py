from fastapi import APIRouter, Depends

from app.auth.oauth2 import verify_token

from app.database import SessionLocal

from app.models.user import User
from app.models.student_profile import StudentProfile

from app.models.degree_program import DegreeProgram
from app.models.cutoff_mark import CutoffMark
from app.models.university import University
from app.models.faculty import Faculty

router = APIRouter()

@router.get("/student/recommendations")
def get_recommendations(

    current_user: str = Depends(verify_token)

):

    db = SessionLocal()

    # Find logged-in user
    user = db.query(User).filter(
        User.email == current_user
    ).first()

    if user is None:

        return {
            "message": "User not found"
        }

    # Find student profile
    student_profile = db.query(StudentProfile).filter(
        StudentProfile.user_id == user.user_id
    ).first()

    if student_profile is None:

        return {
            "message": "Student profile not found"
        }

    # Get student data
    student_stream = student_profile.stream_id

    student_district = student_profile.district_id

    student_zscore = student_profile.z_score

    # Find all degree programs for student's stream
    degrees = db.query(DegreeProgram).filter(
        DegreeProgram.stream_id == student_stream
    ).all()

    recommendations = []

    # Loop through all degrees
    for degree in degrees:

        # Find cutoff mark
        cutoff = db.query(CutoffMark).filter(

            CutoffMark.degree_id == degree.degree_id,

            CutoffMark.district_id == student_district

        ).first()

        # Skip if no cutoff data
        if cutoff is None:
            continue

        # Compare z-score
        if student_zscore >= cutoff.cutoff_zscore:

            # Get university details
            university = db.query(University).filter(
                University.university_id == degree.university_id
            ).first()

            faculty = db.query(Faculty).filter(
                Faculty.faculty_id == degree.faculty_id
            ).first()

            recommendations.append({

                "degree_name": degree.degree_name,

                "faculty": faculty.faculty_name,

                "university": university.university_name,

                "cutoff_zscore": float(cutoff.cutoff_zscore)

            })

    return {

        "student_zscore": student_zscore,

        "recommendations": recommendations
    }