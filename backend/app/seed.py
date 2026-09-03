import json
from .database import SessionLocal
from .models import User, Course, Quiz

def seed_data():
    db = SessionLocal()
    try:
        if db.query(User).count() > 0:
            return
        trainer = User(name="Trainer Demo", email="trainer@skillsphere.com",
                       password_hash="123456", role="trainer",
                       skills=json.dumps({"AWS": 95, "Python": 90, "SQL": 85}))
        trainee = User(name="Trainee Demo", email="trainee@skillsphere.com",
                       password_hash="123456", role="trainee", skills="{}")
        admin = User(name="Admin Demo", email="admin@skillsphere.com",
                     password_hash="123456", role="admin", skills="{}")
        db.add_all([trainer, trainee, admin])
        db.commit()
        db.refresh(trainer)

        courses = [
            Course(title="Python Fundamentals", description="Learn Python basics.",
                   trainer_id=trainer.id, skill_tag="Python", resource_url="#"),
            Course(title="SQL Fundamentals", description="Queries, tables and joins.",
                   trainer_id=trainer.id, skill_tag="Database", resource_url="#"),
            Course(title="AWS Basics", description="Core cloud concepts and AWS services.",
                   trainer_id=trainer.id, skill_tag="Cloud", resource_url="#"),
        ]
        db.add_all(courses)
        db.commit()

        for c in courses:
            questions = [
                ("What does SQL stand for?", ["Structured Query Language", "Simple Query Logic", "System Queue Language"], "Structured Query Language") if c.skill_tag == "Database"
                else ("Which service is object storage in AWS?", ["S3", "EC2", "RDS"], "S3") if c.skill_tag == "Cloud"
                else ("Which keyword defines a function in Python?", ["def", "func", "function"], "def")
            ]
            q, options, answer = questions[0]
            db.add(Quiz(course_id=c.id, question=q, options=json.dumps(options), answer=answer))
        db.commit()
    finally:
        db.close()
