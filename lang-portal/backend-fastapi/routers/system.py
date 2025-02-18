from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict
from database import get_db, engine, Base, WordReviewItem, StudySession, StudyActivity

router = APIRouter(
    prefix="/api",
    tags=["system"],
    responses={404: {"description": "Not found"}},
)

@router.post("/reset_history", response_model=Dict)
def reset_history(db: Session = Depends(get_db)):
    """
    Reset all study history while keeping words and groups intact.
    This deletes all study sessions, activities, and word review items.
    """
    # Delete all word review items
    db.query(WordReviewItem).delete()
    
    # Delete all study sessions
    db.query(StudySession).delete()
    
    # Delete all study activities
    db.query(StudyActivity).delete()
    
    db.commit()
    
    return {
        "success": True,
        "message": "Study history has been reset"
    }

@router.post("/full_reset", response_model=Dict)
def full_reset(db: Session = Depends(get_db)):
    """
    Perform a complete system reset.
    This deletes ALL data including words, groups, and study history.
    """
    # Drop all tables
    Base.metadata.drop_all(bind=engine)
    
    # Recreate all tables
    Base.metadata.create_all(bind=engine)
    
    return {
        "success": True,
        "message": "System has been fully reset"
    }
