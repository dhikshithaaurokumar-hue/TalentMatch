from pathlib import Path
import random

random.seed(42)
base = Path("data/resumes")
base.mkdir(parents=True, exist_ok=True)

skill_sets = [
    ["Python", "SQL", "Machine Learning", "Pandas"],
    ["Java", "HTML", "CSS", "JavaScript"],
    ["Python", "Data Structures", "SQL", "Git"],
    ["Power BI", "Excel", "SQL", "Data Analysis"],
    ["Python", "NLP", "Deep Learning", "TensorFlow"],
    ["React", "JavaScript", "Node.js", "CSS"],
]
degrees = ["B.Tech Computer Science", "B.E. Information Technology", "B.Sc Data Science", "MCA"]
projects = [
    "Built a student performance prediction project.",
    "Created a sales dashboard using sample data.",
    "Developed a simple web application as a college project.",
    "Analyzed public transport data using Python."
]

for i in range(1, 51):
    skills = skill_sets[(i - 1) % len(skill_sets)]
    years = [0, 0.5, 1, 1.5, 2, 3][(i - 1) % 6]
    content = f"""Candidate ID: CANDIDATE_{i:03d}
Education: {degrees[(i - 1) % len(degrees)]}
Experience: {years} years
Skills: {', '.join(skills)}
Projects:
- {projects[(i - 1) % len(projects)]}
"""
    (base / f"candidate_{i:03d}.txt").write_text(content, encoding="utf-8")

jobs = {
    "python_developer.txt": "Python Developer. Required skills: Python, SQL, Machine Learning, Data Structures. Minimum 1 year experience.",
    "data_analyst.txt": "Data Analyst. Required skills: SQL, Excel, Power BI, Data Analysis. Minimum 1 year experience.",
    "frontend_developer.txt": "Frontend Developer. Required skills: HTML, CSS, JavaScript, React. Minimum 1 year experience.",
    "ml_intern.txt": "Machine Learning Intern. Required skills: Python, Machine Learning, Pandas, Deep Learning. Minimum 0 years experience.",
    "backend_developer.txt": "Backend Developer. Required skills: Python, SQL, Django, Git. Minimum 2 years experience."
}
job_dir = Path("data/job_descriptions")
job_dir.mkdir(parents=True, exist_ok=True)
for filename, text in jobs.items():
    (job_dir / filename).write_text(text, encoding="utf-8")

print("Created 50 synthetic resumes and 5 job descriptions.")
