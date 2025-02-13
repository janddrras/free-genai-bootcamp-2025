from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.models import Base
from app.db.session import get_db
from app.initial_data import init_db

# Create a test database in memory
SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create test database and tables
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_create_and_get_word():
    # Create a group first
    group_response = client.post("/api/groups", params={"name": "Test Group"})
    assert group_response.status_code == 200
    group_id = group_response.json()["id"]
    
    # Create a word
    word_data = {
        "hungarian": "test",
        "english": "test",
        "group_ids": [group_id]
    }
    response = client.post("/api/words", params=word_data)
    assert response.status_code == 200
    word_id = response.json()["id"]
    
    # Get the word
    response = client.get(f"/api/words/{word_id}")
    assert response.status_code == 200
    assert response.json()["hungarian"] == "test"
    assert response.json()["english"] == "test"

def test_create_and_get_group():
    # Create a group
    response = client.post("/api/groups", params={"name": "Another Test Group"})
    assert response.status_code == 200
    group_id = response.json()["id"]
    
    # Get the group
    response = client.get(f"/api/groups/{group_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Another Test Group"

def test_dashboard_endpoints():
    # Test last study session endpoint (should return 404 as no sessions exist)
    response = client.get("/api/dashboard/last_study_session")
    assert response.status_code == 404
    
    # Test study progress endpoint
    response = client.get("/api/dashboard/study_progress")
    assert response.status_code == 200
    data = response.json()
    assert "total_words_studied" in data
    assert "total_available_words" in data
    
    # Test quick stats endpoint
    response = client.get("/api/dashboard/quick-stats")
    assert response.status_code == 200
    data = response.json()
    assert "success_rate" in data
    assert "total_study_sessions" in data
    assert "total_active_groups" in data
    assert "study_streak_days" in data 