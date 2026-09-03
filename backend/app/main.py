from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .seed import seed_data
from .routers import auth, courses, quizzes, analytics


# Database
Base.metadata.create_all(bind=engine)
seed_data()


# FastAPI app
app = FastAPI(
    title="SkillSphere API",
    version="1.0.0"
)


# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://skillsphere-frontend-lgrh.onrender.com",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# Routers
# =========================

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


# =========================
# Root
# =========================

@app.get("/")
def root():
    return {
        "message": "SkillSphere API is running"
    }


# =========================
# Health
# =========================

@app.get("/api/health")
def health():
    return {
        "status": "ok"
    }
