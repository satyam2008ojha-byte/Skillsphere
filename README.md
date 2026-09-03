# SkillSphere — SIH26075 CAPACITY CONNECT

Working MVP structure for the SIH internal round.

## MVP flow
Login -> Course -> Enrollment -> Quiz -> Score -> Skill Gap -> Recommendation

## Stack
Frontend: React + Vite
Backend: FastAPI
Database: SQLite by default (easy local demo), PostgreSQL-ready configuration
Smart Engine: Python rule-based skill-gap and recommendation logic
AWS: S3-ready service structure

## Run backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

## Run frontend
cd frontend
npm install
npm run dev

Backend defaults to http://127.0.0.1:8000
Frontend defaults to http://localhost:5173
