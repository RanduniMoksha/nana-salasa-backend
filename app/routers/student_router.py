from fastapi import APIRouter, Depends
from app.auth.oauth2 import verify_token

from app.schemas.student_profile_schema import (
    StudentProfileCreate
    , StudentProfileUpdate
    , StudentProfileResponse
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


@router.get("/student/profile")
def read_profile(
    current_user: str = Depends(verify_token)
):
    """
    Return the current student's profile details.

    - Verifies the token to locate the `User` (by email).
    - Loads the `StudentProfile` for that user and returns its fields.
    - Returns a clear message if the user or profile is not found.
    """

    db = SessionLocal()

    try:

        # Find user by email from the token
        user = db.query(User).filter(
            User.email == current_user
        ).first()

        if user is None:

            return {
                "message": "User not found"
            }

        # Load the student's profile
        profile = db.query(StudentProfile).filter(
            StudentProfile.user_id == user.user_id
        ).first()

        if profile is None:

            return {
                "message": "Student profile not found"
            }

        # Return the profile fields
        return {
            "student_id": profile.student_id,
            "user_id": profile.user_id,
            "stream_id": profile.stream_id,
            "district_id": profile.district_id,
            "z_score": profile.z_score,
            "al_year": profile.al_year
        }

    finally:

        db.close()



@router.put("/student/profile")
def update_profile(
    profile: StudentProfileUpdate,
    current_user: str = Depends(verify_token)
):

    db = SessionLocal()

    try:

        # Find the user by the email returned from token verification
        user = db.query(User).filter(
            User.email == current_user
        ).first()

        if user is None:

            return {
                "message": "User not found"
            }

        # Find existing student profile for this user
        existing = db.query(StudentProfile).filter(
            StudentProfile.user_id == user.user_id
        ).first()

        if existing is None:

            return {
                "message": "Student profile not found"
            }

        # Update only provided fields (partial update behavior)
        if profile.stream_id is not None:
            existing.stream_id = profile.stream_id

        if profile.district_id is not None:
            existing.district_id = profile.district_id

        if profile.z_score is not None:
            existing.z_score = profile.z_score

        if profile.al_year is not None:
            existing.al_year = profile.al_year

        db.add(existing)
        db.commit()

        return {
            "message": "Profile updated",
            "student_id": existing.student_id
        }

    finally:

        db.close()