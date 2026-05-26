from fastapi import APIRouter, Depends
from app.auth.oauth2 import verify_token
from app.database import SessionLocal

from app.models.user import User
from app.models.student_profile import StudentProfile
from app.models.student_result import StudentResult

from app.schemas.student_result_schema import (
    StudentResultCreate,
    StudentResultUpdate
)

from app.models.subject import Subject

router = APIRouter()


@router.post("/student/result")
def add_student_result(

    result: StudentResultCreate,
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

    # Create student result
    new_result = StudentResult(

        student_id=student_profile.student_id,

        subject_id=result.subject_id,

        grade=result.grade
    )

    db.add(new_result)
    db.commit()
    db.refresh(new_result)

    return {

        "message": "Student result added successfully",

        "data": {

            "result_id": new_result.result_id,

            "student_id": new_result.student_id,

            "subject_id": new_result.subject_id,

            "grade": new_result.grade
        }
    }

@router.get("/student/results")
def get_student_results(

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

    # Get all student results
    results = db.query(StudentResult).filter(
        StudentResult.student_id == student_profile.student_id
    ).all()

    output = []

    # Loop through results
    for result in results:

        # Get subject details
        subject = db.query(Subject).filter(
            Subject.subject_id == result.subject_id
        ).first()

        output.append({

            "result_id": result.result_id,

            "subject": subject.subject_name,

            "grade": result.grade
        })

    return {

        "student_id": student_profile.student_id,

        "results": output
    }


@router.put("/student/result/{result_id}")
def update_student_result(

    result_id: int,
    result: StudentResultUpdate,
    current_user: str = Depends(verify_token)
):

    db = SessionLocal()

    try:

        # Verify user from token
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

        # Ensure the result belongs to this student
        existing = db.query(StudentResult).filter(
            StudentResult.result_id == result_id,
            StudentResult.student_id == student_profile.student_id
        ).first()

        if existing is None:

            return {
                "message": "Result not found"
            }

        # Apply partial updates
        if result.subject_id is not None:
            existing.subject_id = result.subject_id

        if result.grade is not None:
            existing.grade = result.grade

        db.add(existing)
        db.commit()
        db.refresh(existing)

        return {
            "message": "Result updated successfully",
            "data": {
                "result_id": existing.result_id,
                "student_id": existing.student_id,
                "subject_id": existing.subject_id,
                "grade": existing.grade
            }
        }

    finally:

        db.close()