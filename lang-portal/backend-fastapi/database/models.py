from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    hungarian = Column(String, index=True)
    english = Column(String, index=True)
    parts = Column(JSON)
    
    groups = relationship('Group', secondary='words_groups', back_populates='words')
    review_items = relationship('WordReviewItem', back_populates='word')

class WordGroup(Base):
    __tablename__ = "words_groups"

    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey('words.id'))
    group_id = Column(Integer, ForeignKey('groups.id'))

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    
    words = relationship('Word', secondary='words_groups', back_populates='groups')
    study_sessions = relationship('StudySession', back_populates='group')
    study_activities = relationship('StudyActivity', back_populates='group')

class StudyActivity(Base):
    __tablename__ = "study_activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, default="Vocabulary Quiz")
    description = Column(String, default="Practice your vocabulary with flashcards")
    group_id = Column(Integer, ForeignKey('groups.id'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    group = relationship('Group', back_populates='study_activities')
    study_sessions = relationship('StudySession', back_populates='study_activity')

class StudySession(Base):
    __tablename__ = "study_sessions"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey('groups.id'))
    study_activity_id = Column(Integer, ForeignKey('study_activities.id'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    end_time = Column(DateTime(timezone=True), nullable=True)
    
    group = relationship('Group', back_populates='study_sessions')
    study_activity = relationship('StudyActivity', back_populates='study_sessions')
    word_review_items = relationship('WordReviewItem', back_populates='study_session')

class WordReviewItem(Base):
    __tablename__ = "word_review_items"

    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey('words.id'))
    study_session_id = Column(Integer, ForeignKey('study_sessions.id'))
    correct = Column(Boolean)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    word = relationship('Word', back_populates='review_items')
    study_session = relationship('StudySession', back_populates='word_review_items')
