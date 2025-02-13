from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app.db.session import get_db
from app.db.models import Group, Word, StudySession

router = APIRouter()

@router.get("")
async def get_groups(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get paginated list of groups."""
    total = db.query(func.count(Group.id)).scalar()
    
    # Get groups with word count
    groups = db.query(Group).offset(skip).limit(limit).all()
    result = []
    
    for group in groups:
        word_count = db.query(func.count(Word.id)).join(
            Group.words
        ).filter(Group.id == group.id).scalar()
        
        result.append({
            "id": group.id,
            "name": group.name,
            "word_count": word_count or 0
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

@router.get("/{group_id}")
async def get_group(group_id: int, db: Session = Depends(get_db)):
    """Get detailed information about a specific group."""
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    # Get total word count
    word_count = db.query(func.count(Word.id)).join(
        Group.words
    ).filter(Group.id == group_id).scalar()
    
    return {
        "id": group.id,
        "name": group.name,
        "stats": {
            "total_word_count": word_count or 0
        }
    }

@router.get("/{group_id}/words")
async def get_group_words(
    group_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get paginated list of words in a group."""
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    total = db.query(func.count(Word.id)).join(Group.words).filter(Group.id == group_id).scalar()
    
    words = db.query(Word).join(Group.words).filter(Group.id == group_id).offset(skip).limit(limit).all()
    
    result = []
    for word in words:
        stats = db.query(
            func.count(Word.id).label('total'),
            func.sum(func.cast(Word.id, 'INTEGER')).label('correct')
        ).filter(Word.id == word.id).first()
        
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

@router.get("/{group_id}/study_sessions")
async def get_group_study_sessions(
    group_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get paginated list of study sessions for a group."""
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    total = db.query(func.count(StudySession.id)).filter(StudySession.group_id == group_id).scalar()
    
    sessions = db.query(StudySession).filter(
        StudySession.group_id == group_id
    ).order_by(StudySession.created_at.desc()).offset(skip).limit(limit).all()
    
    result = []
    for session in sessions:
        review_count = db.query(func.count(Word.id)).join(
            StudySession.word_review_items
        ).filter(StudySession.id == session.id).scalar()
        
        result.append({
            "id": session.id,
            "activity_name": session.study_activity.name,
            "group_name": group.name,
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
async def create_group(name: str, db: Session = Depends(get_db)):
    """Create a new group."""
    # Check if group already exists
    existing = db.query(Group).filter(Group.name == name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Group already exists")
    
    group = Group(name=name)
    db.add(group)
    db.commit()
    db.refresh(group)
    
    return {"id": group.id, "name": group.name}

@router.put("/{group_id}")
async def update_group(group_id: int, name: str, db: Session = Depends(get_db)):
    """Update a group."""
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    # Check if new name already exists
    if name != group.name:
        existing = db.query(Group).filter(Group.name == name).first()
        if existing:
            raise HTTPException(status_code=400, detail="Group name already exists")
    
    group.name = name
    db.commit()
    db.refresh(group)
    
    return {"id": group.id, "name": group.name}

@router.delete("/{group_id}")
async def delete_group(group_id: int, db: Session = Depends(get_db)):
    """Delete a group."""
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    db.delete(group)
    db.commit()
    
    return {"status": "success"} 