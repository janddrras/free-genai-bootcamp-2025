from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, List
from database import get_db, StudyActivity, StudySession, WordReviewItem
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(
    prefix="/api",
    tags=["study"],
    responses={404: {"description": "Not found"}},
)

class StudyActivityCreate(BaseModel):
    group_id: int
    study_activity_id: int

class ReviewCreate(BaseModel):
    correct: bool

@router.get("/study_activities/{activity_id}", response_model=Dict)
def get_study_activity(activity_id: int, db: Session = Depends(get_db)):
    """
    Get details of a specific study activity.
    """
    activity = db.query(StudyActivity).filter(StudyActivity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Study activity not found")
    
    return {
        "id": activity.id,
        "name": "Vocabulary Quiz",  # This should come from activity types table
        "thumbnail_url": "https://example.com/thumbnail.jpg",  # This should come from activity types
        "description": "Practice your vocabulary with flashcards"
    }

@router.get("/study_activities/{activity_id}/study_sessions", response_model=Dict)
def get_activity_sessions(
    activity_id: int, 
    page: int = 1, 
    items_per_page: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get paginated list of study sessions for a specific activity.
    """
    total = db.query(StudySession).filter(StudySession.study_activity_id == activity_id).count()
    sessions = db.query(StudySession).filter(
        StudySession.study_activity_id == activity_id
    ).offset((page - 1) * items_per_page).limit(items_per_page).all()
    
    return {
        "items": [
            {
                "id": session.id,
                "activity_name": "Vocabulary Quiz",  # This should come from activity types
                "group_name": session.group.name,
                "start_time": session.created_at,
                "end_time": None,  # This needs to be added to the model
                "review_items_count": len(session.word_review_items)
            }
            for session in sessions
        ],
        "pagination": {
            "current_page": page,
            "total_pages": (total + items_per_page - 1) // items_per_page,
            "total_items": total,
            "items_per_page": items_per_page
        }
    }

@router.post("/study_activities", response_model=Dict)
def create_study_activity(
    activity: StudyActivityCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new study activity.
    """
    db_activity = StudyActivity(
        group_id=activity.group_id,
        study_activity_id=activity.study_activity_id
    )
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    
    return {
        "id": db_activity.id,
        "group_id": db_activity.group_id
    }

@router.post("/study_sessions/{session_id}/words/{word_id}/review", response_model=Dict)
def create_word_review(
    session_id: int,
    word_id: int,
    review: ReviewCreate,
    db: Session = Depends(get_db)
):
    """
    Create a review for a word in a study session.
    """
    # Verify session exists
    session = db.query(StudySession).filter(StudySession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Study session not found")
    
    review_item = WordReviewItem(
        word_id=word_id,
        study_session_id=session_id,
        correct=review.correct
    )
    db.add(review_item)
    db.commit()
    
    return {"status": "success"}
