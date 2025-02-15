from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, List
from database import get_db, Word, WordReviewItem
from sqlalchemy.sql import func

router = APIRouter(
    prefix="/api",
    tags=["words"],
    responses={404: {"description": "Not found"}},
)

@router.get("/words", response_model=Dict)
def get_words(
    page: int = 1,
    items_per_page: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get paginated list of words with their statistics.
    """
    total = db.query(Word).count()
    words = db.query(Word).offset((page - 1) * items_per_page).limit(items_per_page).all()
    
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

@router.get("/words/{word_id}", response_model=Dict)
def get_word(word_id: int, db: Session = Depends(get_db)):
    """
    Get details of a specific word including its statistics and groups.
    """
    word = db.query(Word).filter(Word.id == word_id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    
    correct = db.query(func.count(WordReviewItem.id)).filter(
        WordReviewItem.word_id == word.id,
        WordReviewItem.correct == True
    ).scalar()
    wrong = db.query(func.count(WordReviewItem.id)).filter(
        WordReviewItem.word_id == word.id,
        WordReviewItem.correct == False
    ).scalar()
    
    return {
        "hungarian": word.hungarian,
        "english": word.english,
        "stats": {
            "correct_count": correct,
            "wrong_count": wrong
        },
        "groups": [
            {
                "id": group.id,
                "name": group.name
            }
            for group in word.groups
        ]
    }
