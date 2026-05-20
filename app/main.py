from fastapi import FastAPI

from app.routers import auth_router

from app.routers import student_router

from app.models.user import User
from app.models.student_profile import StudentProfile
from app.models.stream import Stream
from app.models.district import District

app = FastAPI()

app.include_router(auth_router.router)
app.include_router(student_router.router)


@app.get("/")
def home():

    return {"message": "Backend is running"}