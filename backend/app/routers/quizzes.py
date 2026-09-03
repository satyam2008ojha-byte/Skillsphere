import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Quiz, Result
from ..schemas import QuizSubmit
from ..services.smart_engine import detect_skill_gap, recommend_courses

router = APIRouter(prefix="/quizzes", tags=["Quizzes"])

@router.get("/{course_id}")
def get_quiz(course_id: int, db: Session = Depends(get_db)):
    qs = db.query(Quiz).filter(Quiz.course_id == course_id).all()
    return [{"id": q.id, "question": q.question, "options": json.loads(q.options)} for q in qs]

@router.post("/submit")
def submit_quiz(data: QuizSubmit, db: Session = Depends(get_db)):
    qs = db.query(Quiz).filter(Quiz.course_id == data.course_id).all()
    if not qs:
        raise HTTPException(status_code=404, detail="Quiz not found")
    correct = sum(1 for q, a in zip(qs, data.answers) if q.answer == a)
    score = round(correct / len(qs) * 100, 2)
    course_skill = {"1": "Python", "2": "Database", "3": "Cloud"}.get(str(data.course_id), "General")
    weak = detect_skill_gap(score, course_skill)
    db.add(Result(user_id=data.user_id, quiz_id=qs[0].id, score=score, weak_skill=weak))
    db.commit()
    return {"score": score, "weak_skill": weak,
            "recommendations": recommend_courses(weak)}
