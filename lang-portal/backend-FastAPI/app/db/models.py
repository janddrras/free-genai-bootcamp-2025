from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Association table for many-to-many relationship between words and groups
words_groups = Table(
    'words_groups',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('word_id', Integer, ForeignKey('words.id')),
    Column('group_id', Integer, ForeignKey('groups.id'))
)

class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    hungarian = Column(String, index=True)
    english = Column(String, index=True)
    parts = Column(JSON)
    
    # Relationships
    groups = relationship("Group", secondary=words_groups, back_populates="words")
    review_items = relationship("WordReviewItem", back_populates="word")

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    
    # Relationships
    words = relationship("Word", secondary=words_groups, back_populates="groups")
    study_sessions = relationship("StudySession", back_populates="group")
    study_activities = relationship("StudyActivity", back_populates="group")

class StudySession(Base):
    __tablename__ = "study_sessions"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    study_activity_id = Column(Integer, ForeignKey("study_activities.id"))
    
    # Relationships
    group = relationship("Group", back_populates="study_sessions")
    study_activity = relationship("StudyActivity", back_populates="study_sessions")
    word_review_items = relationship("WordReviewItem", back_populates="study_session")

class StudyActivity(Base):
    __tablename__ = "study_activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    thumbnail_url = Column(String)
    description = Column(String)
    group_id = Column(Integer, ForeignKey("groups.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    group = relationship("Group", back_populates="study_activities")
    study_sessions = relationship("StudySession", back_populates="study_activity")

class WordReviewItem(Base):
    __tablename__ = "word_review_items"

    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey("words.id"))
    study_session_id = Column(Integer, ForeignKey("study_sessions.id"))
    correct = Column(Boolean)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    word = relationship("Word", back_populates="review_items")
    study_session = relationship("StudySession", back_populates="word_review_items") 