from fastapi import APIRouter
from app.api.api_v1.endpoints import (
    dashboard,
    words,
    groups,
    study_sessions,
    study_activities,
    system
)

api_router = APIRouter()

api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(words.router, prefix="/words", tags=["words"])
api_router.include_router(groups.router, prefix="/groups", tags=["groups"])
api_router.include_router(study_sessions.router, prefix="/study_sessions", tags=["study_sessions"])
api_router.include_router(study_activities.router, prefix="/study_activities", tags=["study_activities"])
api_router.include_router(system.router, prefix="/system", tags=["system"]) 