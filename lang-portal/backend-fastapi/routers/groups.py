from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, List
from database import get_db, Group, Word, StudySession, WordReviewItem
from sqlalchemy.sql import func

router = APIRouter(
    prefix="/api",
    tags=["groups"],
    responses={404: {"description": "Not found"}},
)

@router.get("/groups", response_model=Dict)
def get_groups(
    page: int = 1,
    items_per_page: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get paginated list of groups with word counts.
    """
    total = db.query(Group).count()
    groups = db.query(Group).offset((page - 1) * items_per_page).limit(items_per_page).all()
    
    return {
        "items": [
            {
                "id": group.id,
                "name": group.name,
                "word_count": len(group.words)
            }
            for group in groups
        ],
        "pagination": {
            "current_page": page,
            "total_pages": (total + items_per_page - 1) // items_per_page,
            "total_items": total,
            "items_per_page": items_per_page
        }
    }

@router.get("/groups/{group_id}", response_model=Dict)
def get_group(group_id: int, db: Session = Depends(get_db)):
    """
    Get details of a specific group including statistics.
    """
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    return {
        "id": group.id,
        "name": group.name,
        "stats": {
            "total_word_count": len(group.words)
        }
    }

@router.get("/groups/{group_id}/words", response_model=Dict)
def get_group_words(
    group_id: int,
    page: int = 1,
    items_per_page: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get paginated list of words in a specific group with their statistics.
    """
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    total = len(group.words)
    words = group.words[(page - 1) * items_per_page:page * items_per_page]
    
    word_stats = {}
    for word in words:
        correct = db.query(func.count(WordReviewItem.id)).filter(
            WordReviewItem.word_id == word.id,
            WordReviewItem.correct == True
        ).scalar()
        wrong = db.query(func.count(WordReviewItem.id)).filter(
            WordReviewItem.word_id == word.id,
            WordReviewItem.correct == False
        ).scalar()
        word_stats[word.id] = {"correct": correct, "wrong": wrong}
    
    return {
        "items": [
            {
                "hungarian": word.hungarian,
                "english": word.english,
                "correct_count": word_stats[word.id]["correct"],
                "wrong_count": word_stats[word.id]["wrong"]
            }
            for word in words
        ],
        "pagination": {
            "current_page": page,
            "total_pages": (total + items_per_page - 1) // items_per_page,
            "total_items": total,
            "items_per_page": items_per_page
        }
    }

@router.get("/groups/{group_id}/study_sessions", response_model=Dict)
def get_group_sessions(
    group_id: int,
    page: int = 1,
    items_per_page: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get paginated list of study sessions for a specific group.
    """
    total = db.query(StudySession).filter(StudySession.group_id == group_id).count()
    sessions = db.query(StudySession).filter(
        StudySession.group_id == group_id
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
