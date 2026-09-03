COURSES = {
    "Python": ["Python Fundamentals"],
    "Database": ["SQL Fundamentals"],
    "Cloud": ["AWS Basics"],
}

def detect_skill_gap(score: float, skill: str):
    # SIH MVP rule: score < 50% => skill gap
    return skill if score < 50 else None

def recommend_courses(weak_skill):
    if not weak_skill:
        return []
    return COURSES.get(weak_skill, [])
