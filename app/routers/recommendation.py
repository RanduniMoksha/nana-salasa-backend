from fastapi import APIRouter, Depends

from app.auth.oauth2 import verify_token

from app.database import SessionLocal

from app.models.user import User
from app.models.student_profile import StudentProfile

from app.models.degree_program import DegreeProgram
from app.models.cutoff_mark import CutoffMark
from app.models.university import University
from app.models.degree_streams import DegreeStream

from app.services.eligibility_service import (
    check_subject_requirements
)

router = APIRouter()


@router.get("/student/recommendations")
def get_recommendations(

    current_user: str = Depends(verify_token)

):

    db = SessionLocal()

    try:

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

        # First-stage filtering
        recommendations_query = (

            db.query(

                DegreeProgram.degree_id,

                DegreeProgram.degree_name,

                University.university_name,

                CutoffMark.cutoff_zscore

            )

            .join(
                DegreeStream,
                DegreeProgram.degree_id == DegreeStream.degree_id
            )

            .join(
                CutoffMark,
                DegreeProgram.degree_id == CutoffMark.degree_id
            )

            .join(
                University,
                DegreeProgram.university_id == University.university_id
            )

            .filter(
                DegreeStream.stream_id == student_stream
            )

            .filter(
                CutoffMark.district_id == student_district
            )

            .filter(
                CutoffMark.cutoff_zscore <= student_zscore
            )

            .order_by(
                CutoffMark.cutoff_zscore.desc()
            )

            .all()
        )

        recommendations = []

        # Second-stage filtering
        # Subject requirement validation

        for item in recommendations_query:

            eligible = check_subject_requirements(

                db=db,
                student_profile=student_profile,
                degree_id=item.degree_id

            )

            if eligible:

                recommendations.append({

                    "degree_id": item.degree_id,

                    "degree_name": item.degree_name,

                    "university": item.university_name,

                    "cutoff_zscore": float(
                        item.cutoff_zscore
                    )

                })

        return {

            "student_zscore": student_zscore,

            "total_recommendations": len(recommendations),

            "recommendations": recommendations

        }

    finally:

        db.close()