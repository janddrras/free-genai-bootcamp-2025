from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine, get_settings
from routers import dashboard, study, words, groups, system

# Get settings
settings = get_settings()

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.ALLOWED_METHODS,
    allow_headers=settings.ALLOWED_HEADERS,
)

# Include routers
app.include_router(dashboard.router)
app.include_router(study.router)
app.include_router(words.router)
app.include_router(groups.router)
app.include_router(system.router)

@app.get("/")
async def root():
    """
    Root endpoint returning API information.
    """
    return {
        "app": "Language Learning Portal API",
        "version": "1.0.0",
        "documentation": "/docs"
    }
