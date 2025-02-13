from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime, timedelta

from app.db.session import get_db
from app.db.models import StudySession, WordReviewItem, Group, Word

router = APIRouter()

@router.get("/last_study_session")
async def get_last_study_session(db: Session = Depends(get_db)):
    """Get information about the most recent study session."""
    last_session = db.query(StudySession).order_by(StudySession.created_at.desc()).first()
    
    if not last_session:
        raise HTTPException(status_code=404, detail="No study sessions found")
    
    return {
        "id": last_session.id,
        "group_id": last_session.group_id,
        "created_at": last_session.created_at,
        "study_activity_id": last_session.study_activity_id,
        "group_name": last_session.group.name
    }

@router.get("/study_progress")
async def get_study_progress(db: Session = Depends(get_db)):
    """Get study progress statistics."""
    total_words = db.query(func.count(Word.id)).scalar()
    studied_words = db.query(func.count(func.distinct(WordReviewItem.word_id))).scalar()
    
    return {
        "total_words_studied": studied_words or 0,
        "total_available_words": total_words or 0
    }

@router.get("/quick-stats")
async def get_quick_stats(db: Session = Depends(get_db)):
    """Get quick overview statistics."""
    # Calculate success rate
    review_stats = db.query(
        func.count(WordReviewItem.id).label('total'),
        func.sum(func.cast(WordReviewItem.correct, 'INTEGER')).label('correct')
    ).first()
    
    success_rate = 0
    if review_stats.total:
        success_rate = (review_stats.correct or 0) / review_stats.total * 100
    
    # Count total study sessions
    total_sessions = db.query(func.count(StudySession.id)).scalar() or 0
    
    # Count active groups (groups with at least one study session in the last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    active_groups = db.query(func.count(func.distinct(StudySession.group_id))).filter(
        StudySession.created_at >= thirty_days_ago
    ).scalar() or 0
    
    # Calculate study streak
    current_streak = 0
    last_session = db.query(StudySession).order_by(StudySession.created_at.desc()).first()
    
    if last_session:
        current_date = last_session.created_at.date()
        streak_broken = False
        
        while not streak_broken:
            session_exists = db.query(StudySession).filter(
                func.date(StudySession.created_at) == current_date
            ).first() is not None
            
            if session_exists:
                current_streak += 1
                current_date -= timedelta(days=1)
            else:
                streak_broken = True
    
    return {
        "success_rate": round(success_rate, 1),
        "total_study_sessions": total_sessions,
        "total_active_groups": active_groups,
        "study_streak_days": current_streak
    } 