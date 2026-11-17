import re
from resume_parser import SKILL_VOCABULARY

def analyze_job(text: str) -> dict:
    low = text.lower()
    skills = sorted({s for s in SKILL_VOCABULARY if re.search(r"(?<!\w)" + re.escape(s) + r"(?!\w)", low)})
    # Treat detected skills as required for this starter version; recruiter should verify.
    exp = re.search(r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)", low)
    min_years = float(exp.group(1)) if exp else 0.0
    return {"required_skills": skills, "min_experience_years": min_years, "raw_text": text}
