from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, Course, Result

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("")
def analytics(db: Session = Depends(get_db)):
    results = db.query(Result).all()
    avg = round(sum(r.score or 0 for r in results) / len(results), 2) if results else 0
    return {"users": db.query(User).count(), "courses": db.query(Course).count(),
            "attempts": len(results), "average_score": avg}
