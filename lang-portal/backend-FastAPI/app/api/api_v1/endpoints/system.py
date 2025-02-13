from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db, engine
from app.db.models import Base
from app.db.models import WordReviewItem, StudySession

router = APIRouter()

@router.post("/reset_history")
async def reset_history(db: Session = Depends(get_db)):
    """Reset all study history."""
    # Delete all word review items
    db.query(WordReviewItem).delete()
    # Delete all study sessions
    db.query(StudySession).delete()
    db.commit()
    
    return {
        "success": True,
        "message": "Study history has been reset"
    }

@router.post("/full_reset")
async def full_reset(db: Session = Depends(get_db)):
    """Drop all tables and recreate them."""
    # Drop all tables
    Base.metadata.drop_all(bind=engine)
    # Recreate all tables
    Base.metadata.create_all(bind=engine)
    
    return {
        "success": True,
        "message": "System has been fully reset"
    } 