from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app.db.session import get_db
from app.db.models import StudyActivity, StudySession

router = APIRouter()

@router.get("/{activity_id}")
async def get_study_activity(activity_id: int, db: Session = Depends(get_db)):
    """Get information about a specific study activity."""
    activity = db.query(StudyActivity).filter(StudyActivity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Study activity not found")
    
    return {
        "id": activity.id,
        "name": activity.name,
        "thumbnail_url": activity.thumbnail_url,
        "description": activity.description
    }

@router.get("/{activity_id}/study_sessions")
async def get_activity_study_sessions(
    activity_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get paginated list of study sessions for an activity."""
    activity = db.query(StudyActivity).filter(StudyActivity.id == activity_id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Study activity not found")
    
    total = db.query(func.count(StudySession.id)).filter(
        StudySession.study_activity_id == activity_id
    ).scalar()
    
    sessions = db.query(StudySession).filter(
        StudySession.study_activity_id == activity_id
    ).order_by(StudySession.created_at.desc()).offset(skip).limit(limit).all()
    
    result = []
    for session in sessions:
        review_count = db.query(func.count(StudySession.word_review_items)).filter(
            StudySession.id == session.id
        ).scalar()
        
        result.append({
            "id": session.id,
            "activity_name": activity.name,
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

@router.post("")
async def create_study_activity(
    name: str,
    group_id: int,
    thumbnail_url: Optional[str] = None,
    description: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Create a new study activity."""
    activity = StudyActivity(
        name=name,
        group_id=group_id,
        thumbnail_url=thumbnail_url,
        description=description
    )
    db.add(activity)
    db.commit()
    db.refresh(activity)
    
    return {
        "id": activity.id,
        "name": activity.name,
        "thumbnail_url": activity.thumbnail_url,
        "description": activity.description
    } 