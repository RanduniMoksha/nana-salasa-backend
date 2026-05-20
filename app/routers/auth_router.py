from fastapi import APIRouter

from app.database import SessionLocal

from app.models.user import User

from app.schemas.user_schema import UserCreate

from app.schemas.auth_schema import LoginRequest

from app.auth.password_handler import (
    hash_password,
    verify_password
)

from app.auth.jwt_handler import create_access_token

from app.auth.oauth2 import verify_token

from fastapi import Depends


router = APIRouter()


@router.post("/register")
def register(user: UserCreate):

    db = SessionLocal()

    new_user = User(
        full_name=user.full_name,
        email=user.email,
        password_hash=hash_password(user.password)
    )

    db.add(new_user)

    db.commit()

    return {
        "message": "User registered successfully"
    }


@router.post("/login")
def login(user: LoginRequest):

    db = SessionLocal()

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user is None:

        return {
            "message": "User not found"
        }

    if not verify_password(
        user.password,
        existing_user.password_hash
    ):

        return {
            "message": "Incorrect password"
        }

    token = create_access_token(
        data={"sub": existing_user.email}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/profile")
def profile(current_user: str = Depends(verify_token)):

    return {
        "message": "Protected route",
        "user": current_user
    }