from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models import Word, Group, StudyActivity

def init_db(db: Session) -> None:
    # Create sample groups
    basic_greetings = Group(name="Basic Greetings")
    numbers = Group(name="Numbers")
    common_verbs = Group(name="Common Verbs")
    
    db.add_all([basic_greetings, numbers, common_verbs])
    db.flush()
    
    # Create sample words for Basic Greetings
    greetings = [
        Word(hungarian="szia", english="hello", parts={"type": "greeting", "formality": "informal"}),
        Word(hungarian="jó reggelt", english="good morning", parts={"type": "greeting", "time": "morning"}),
        Word(hungarian="jó napot", english="good day", parts={"type": "greeting", "time": "day"}),
        Word(hungarian="jó estét", english="good evening", parts={"type": "greeting", "time": "evening"}),
        Word(hungarian="viszlát", english="goodbye", parts={"type": "farewell", "formality": "informal"})
    ]
    for word in greetings:
        word.groups.append(basic_greetings)
    
    # Create sample words for Numbers
    numbers_words = [
        Word(hungarian="egy", english="one", parts={"type": "number", "value": 1}),
        Word(hungarian="kettő", english="two", parts={"type": "number", "value": 2}),
        Word(hungarian="három", english="three", parts={"type": "number", "value": 3}),
        Word(hungarian="négy", english="four", parts={"type": "number", "value": 4}),
        Word(hungarian="öt", english="five", parts={"type": "number", "value": 5})
    ]
    for word in numbers_words:
        word.groups.append(numbers)
    
    # Create sample words for Common Verbs
    verbs = [
        Word(hungarian="lenni", english="to be", parts={"type": "verb", "category": "essential"}),
        Word(hungarian="menni", english="to go", parts={"type": "verb", "category": "motion"}),
        Word(hungarian="enni", english="to eat", parts={"type": "verb", "category": "action"}),
        Word(hungarian="inni", english="to drink", parts={"type": "verb", "category": "action"}),
        Word(hungarian="aludni", english="to sleep", parts={"type": "verb", "category": "state"})
    ]
    for word in verbs:
        word.groups.append(common_verbs)
    
    db.add_all(greetings + numbers_words + verbs)
    
    # Create sample study activities
    activities = [
        StudyActivity(
            name="Flashcards",
            description="Practice vocabulary with flashcards",
            thumbnail_url="/static/images/flashcards.png",
            group_id=basic_greetings.id
        ),
        StudyActivity(
            name="Multiple Choice",
            description="Test your knowledge with multiple choice questions",
            thumbnail_url="/static/images/multiple-choice.png",
            group_id=numbers.id
        ),
        StudyActivity(
            name="Writing Practice",
            description="Practice writing words and phrases",
            thumbnail_url="/static/images/writing.png",
            group_id=common_verbs.id
        )
    ]
    db.add_all(activities)
    
    db.commit()

def main() -> None:
    db = SessionLocal()
    init_db(db)

if __name__ == "__main__":
    main() 