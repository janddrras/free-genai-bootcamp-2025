from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.db.session import get_db
from app.db.models import StudySession, Word, WordReviewItem

router = APIRouter()

@router.get("")
async def get_study_sessions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get paginated list of study sessions."""
    total = db.query(func.count(StudySession.id)).scalar()
    
    sessions = db.query(StudySession).order_by(
        StudySession.created_at.desc()
    ).offset(skip).limit(limit).all()
    
    result = []
    for session in sessions:
        review_count = db.query(func.count(WordReviewItem.id)).filter(
            WordReviewItem.study_session_id == session.id
        ).scalar()
        
        result.append({
            "id": session.id,
            "activity_name": session.study_activity.name,
            "group_name": session.group.name,
            "start_time": session.created_at,
            "end_time": None,  # We don't track end time in our current model
            "review_items_count": review_count or 0
        })
    
    return {
        "items": result,
        "pagination": {
            "current_page": skip // limit + 1,
            "total_pages": (total + limit - 1) // limit,
            "total_items": total,
            "items_per_page": limit
        }
    }

@router.get("/{session_id}")
async def get_study_session(session_id: int, db: Session = Depends(get_db)):
    """Get detailed information about a specific study session."""
    session = db.query(StudySession).filter(StudySession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Study session not found")
    
    review_count = db.query(func.count(WordReviewItem.id)).filter(
        WordReviewItem.study_session_id == session.id
    ).scalar()
    
    return {
        "id": session.id,
        "activity_name": session.study_activity.name,
        "group_name": session.group.name,
        "start_time": session.created_at,
        "end_time": None,  # We don't track end time in our current model
        "review_items_count": review_count or 0
    }

@router.get("/{session_id}/words")
async def get_session_words(
    session_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get paginated list of words reviewed in a study session."""
    session = db.query(StudySession).filter(StudySession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Study session not found")
    
    total = db.query(func.count(Word.id)).join(WordReviewItem).filter(
        WordReviewItem.study_session_id == session_id
    ).scalar()
    
    words = db.query(Word).join(WordReviewItem).filter(
        WordReviewItem.study_session_id == session_id
    ).offset(skip).limit(limit).all()
    
    result = []
    for word in words:
        stats = db.query(
            func.count(WordReviewItem.id).label('total'),
            func.sum(func.cast(WordReviewItem.correct, 'INTEGER')).label('correct')
        ).filter(WordReviewItem.word_id == word.id).first()
        
        result.append({
            "hungarian": word.hungarian,
            "english": word.english,
            "correct_count": stats.correct or 0,
            "wrong_count": (stats.total or 0) - (stats.correct or 0)
        })
    
    return {
        "items": result,
        "pagination": {
            "current_page": skip // limit + 1,
            "total_pages": (total + limit - 1) // limit,
            "total_items": total,
            "items_per_page": limit
        }
    }

@router.post("/{session_id}/words/{word_id}/review")
async def create_word_review(
    session_id: int,
    word_id: int,
    correct: bool,
    db: Session = Depends(get_db)
):
    """Create a word review for a study session."""
    # Verify session exists
    session = db.query(StudySession).filter(StudySession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Study session not found")
    
    # Verify word exists
    word = db.query(Word).filter(Word.id == word_id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    
    # Create review
    review = WordReviewItem(
        word_id=word_id,
        study_session_id=session_id,
        correct=correct
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    
    return {
        "success": True,
        "word_id": word_id,
        "study_session_id": session_id,
        "correct": correct,
        "created_at": review.created_at
    } 