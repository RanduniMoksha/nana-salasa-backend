from fastapi import APIRouter, Depends

from app.auth.oauth2 import verify_token

from app.schemas.student_profile_schema import (
    StudentProfileCreate
)

from app.models.student_profile import StudentProfile
from app.models.user import User

from app.database import SessionLocal

router = APIRouter()

@router.get("/student/test")
def student_test(
    current_user: str = Depends(verify_token)
):

    return {
        "message": "Student router works",
        "user": current_user
    }

@router.post("/student/profile")
def create_profile(
    profile: StudentProfileCreate,
    current_user: str = Depends(verify_token)
):

    db = SessionLocal()

    user = db.query(User).filter(
        User.email == current_user
    ).first()

    if user is None:

        return {
            "message": "User not found"
        }

    new_profile = StudentProfile(

        user_id=user.user_id,

        stream_id=profile.stream_id,

        district_id=profile.district_id,

        z_score=profile.z_score,

        al_year=profile.al_year
    )

    db.add(new_profile)

    db.commit()

    return {
        "message": "Profile created"
    }