from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .seed import seed_data
from .routers import auth, courses, quizzes, analytics


# Create database tables
Base.metadata.create_all(bind=engine)

# Add initial/demo data
seed_data()


# Create FastAPI application
app = FastAPI(
    title="SkillSphere API",
    version="1.0.0"
)


# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://skillsphere-frontend-lgrh.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# API Routers
app.include_router(
    auth.router,
    prefix="/api"
)

app.include_router(
    courses.router,
    prefix="/api"
)

app.include_router(
    quizzes.router,
    prefix="/api"
)

app.include_router(
    analytics.router,
    prefix="/api"
)


# Root endpoint
@app.get("/")
def root():
    return {
        "message": "SkillSphere API is running"
    }


# Health check endpoint
@app.get("/api/health")
def health():
    return {
        "status": "ok"
    }
