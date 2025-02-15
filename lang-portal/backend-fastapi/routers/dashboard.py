from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict
from database import get_db, StudySession, Group, WordReviewItem, Word
from sqlalchemy.sql import func
from sqlalchemy import desc

router = APIRouter(
    prefix="/api/dashboard",
    tags=["dashboard"],
    responses={404: {"description": "Not found"}},
)

@router.get("/last_study_session", response_model=Dict)
def get_last_study_session(db: Session = Depends(get_db)):
    """
    Returns information about the most recent study session.
    """
    last_session = db.query(StudySession).join(Group).order_by(desc(StudySession.created_at)).first()
    if not last_session:
        return {}
    
    return {
        "id": last_session.id,
        "group_id": last_session.group_id,
        "created_at": last_session.created_at,
        "study_activity_id": last_session.study_activity_id,
        "group_name": last_session.group.name
    }

@router.get("/study_progress", response_model=Dict)
def get_study_progress(db: Session = Depends(get_db)):
    """
    Returns study progress statistics including total words studied and available.
    """
    total_words_studied = db.query(func.count(WordReviewItem.word_id.distinct())).scalar()
    total_available_words = db.query(func.count(Word.id)).scalar()
    
    return {
        "total_words_studied": total_words_studied,
        "total_available_words": total_available_words
    }

@router.get("/quick-stats", response_model=Dict)
def get_quick_stats(db: Session = Depends(get_db)):
    """
    Returns quick overview statistics including success rate, total sessions, active groups, and streak.
    """
    total_reviews = db.query(WordReviewItem).count()
    correct_reviews = db.query(WordReviewItem).filter(WordReviewItem.correct == True).count()
    success_rate = (correct_reviews / total_reviews * 100) if total_reviews > 0 else 0
    
    total_study_sessions = db.query(StudySession).count()
    total_active_groups = db.query(Group).count()
    
    # TODO: Implement study streak calculation
    study_streak_days = 0  # This needs more complex logic with date calculations
    
    return {
        "success_rate": round(success_rate, 1),
        "total_study_sessions": total_study_sessions,
        "total_active_groups": total_active_groups,
        "study_streak_days": study_streak_days
    }
