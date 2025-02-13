from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from app.db.session import get_db
from app.db.models import Word, WordReviewItem, Group

router = APIRouter()

@router.get("")
async def get_words(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get paginated list of words with their review statistics."""
    total = db.query(func.count(Word.id)).scalar()
    
    words = db.query(Word).offset(skip).limit(limit).all()
    
    # Get review statistics for each word
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

@router.get("/{word_id}")
async def get_word(word_id: int, db: Session = Depends(get_db)):
    """Get detailed information about a specific word."""
    word = db.query(Word).filter(Word.id == word_id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    
    # Get review statistics
    stats = db.query(
        func.count(WordReviewItem.id).label('total'),
        func.sum(func.cast(WordReviewItem.correct, 'INTEGER')).label('correct')
    ).filter(WordReviewItem.word_id == word_id).first()
    
    return {
        "hungarian": word.hungarian,
        "english": word.english,
        "stats": {
            "correct_count": stats.correct or 0,
            "wrong_count": (stats.total or 0) - (stats.correct or 0)
        },
        "groups": [{"id": group.id, "name": group.name} for group in word.groups]
    }

@router.post("")
async def create_word(
    hungarian: str,
    english: str,
    parts: Optional[dict] = None,
    group_ids: List[int] = Query(None),
    db: Session = Depends(get_db)
):
    """Create a new word."""
    # Check if word already exists
    existing = db.query(Word).filter(
        (Word.hungarian == hungarian) | (Word.english == english)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Word already exists")
    
    # Create new word
    word = Word(hungarian=hungarian, english=english, parts=parts)
    db.add(word)
    db.flush()
    
    # Add to groups if specified
    if group_ids:
        groups = db.query(Group).filter(Group.id.in_(group_ids)).all()
        if len(groups) != len(group_ids):
            raise HTTPException(status_code=400, detail="One or more groups not found")
        word.groups = groups
    
    db.commit()
    return {"id": word.id, "hungarian": word.hungarian, "english": word.english}

@router.put("/{word_id}")
async def update_word(
    word_id: int,
    hungarian: Optional[str] = None,
    english: Optional[str] = None,
    parts: Optional[dict] = None,
    group_ids: List[int] = Query(None),
    db: Session = Depends(get_db)
):
    """Update a word."""
    word = db.query(Word).filter(Word.id == word_id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    
    # Update fields if provided
    if hungarian is not None:
        word.hungarian = hungarian
    if english is not None:
        word.english = english
    if parts is not None:
        word.parts = parts
    
    # Update groups if provided
    if group_ids is not None:
        groups = db.query(Group).filter(Group.id.in_(group_ids)).all()
        if len(groups) != len(group_ids):
            raise HTTPException(status_code=400, detail="One or more groups not found")
        word.groups = groups
    
    db.commit()
    return {"id": word.id, "hungarian": word.hungarian, "english": word.english}

@router.delete("/{word_id}")
async def delete_word(word_id: int, db: Session = Depends(get_db)):
    """Delete a word."""
    word = db.query(Word).filter(Word.id == word_id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    
    db.delete(word)
    db.commit()
    return {"status": "success"} 