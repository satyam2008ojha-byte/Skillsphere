from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Course, Enrollment
from ..schemas import EnrollmentRequest

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.get("")
def list_courses(db: Session = Depends(get_db)):
    courses = db.query(Course).all()
    return [{"id": c.id, "title": c.title, "description": c.description,
             "skill_tag": c.skill_tag, "resource_url": c.resource_url} for c in courses]

@router.post("/enroll")
def enroll(data: EnrollmentRequest, db: Session = Depends(get_db)):
    existing = db.query(Enrollment).filter_by(user_id=data.user_id, course_id=data.course_id).first()
    if existing:
        return {"message": "Already enrolled"}
    e = Enrollment(user_id=data.user_id, course_id=data.course_id)
    db.add(e)
    db.commit()
    return {"message": "Enrolled successfully"}
