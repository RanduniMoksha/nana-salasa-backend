from fastapi import FastAPI

from app.routers import auth_router

from app.routers import student_router

from app.routers import student_result

from app.routers import recommendation

from app.models.user import User
from app.models.student_profile import StudentProfile
from app.models.stream import Stream
from app.models.district import District
from app.models.subject import Subject
from app.models.degree_program import DegreeProgram
from app.models.cutoff_mark import CutoffMark
from app.models.university import University
from app.models.student_result import StudentResult
from app.models.faculty import Faculty
from app.models.degree_streams import DegreeStream


app = FastAPI()

app.include_router(auth_router.router)
app.include_router(student_router.router)
app.include_router(student_result.router)
app.include_router(recommendation.router)

@app.get("/")
def home():

    return {"message": "Backend is running"}