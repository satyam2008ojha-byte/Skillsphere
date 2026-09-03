from pydantic import BaseModel
from typing import List

class LoginRequest(BaseModel):
    email: str
    password: str

class EnrollmentRequest(BaseModel):
    user_id: int
    course_id: int

class QuizSubmit(BaseModel):
    user_id: int
    course_id: int
    answers: List[str]
