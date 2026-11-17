import re
from pathlib import Path

SKILL_VOCABULARY = [
    "python", "java", "c++", "sql", "machine learning", "deep learning",
    "data analysis", "pandas", "numpy", "tensorflow", "pytorch",
    "html", "css", "javascript", "react", "node.js", "django", "flask",
    "communication", "project management", "excel", "power bi",
    "natural language processing", "nlp", "computer vision", "git",
    "aws", "azure", "docker", "kubernetes", "data structures"
]

def extract_text(data: bytes, filename: str) -> str:
    ext = Path(filename).suffix.lower()
    if ext == ".pdf":
        import fitz
        doc = fitz.open(stream=data, filetype="pdf")
        return "\n".join(page.get_text() for page in doc)
    if ext == ".docx":
        from docx import Document
        import io
        doc = Document(io.BytesIO(data))
        return "\n".join(p.text for p in doc.paragraphs)
    if ext == ".txt":
        return data.decode("utf-8", errors="ignore")
    raise ValueError("Supported formats are PDF, DOCX and TXT.")

def parse_resume(data: bytes, filename: str) -> dict:
    text = extract_text(data, filename)
    low = text.lower()
    skills = sorted({s for s in SKILL_VOCABULARY if re.search(r"(?<!\w)" + re.escape(s) + r"(?!\w)", low)})
    # Heuristic extraction: this is a baseline parser, not a perfect CV understanding model.
    exp_values = re.findall(r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)", low)
    experience = max([float(x) for x in exp_values], default=0.0)
    education_terms = ["b.e", "b.tech", "bachelor", "b.sc", "m.e", "m.tech", "master", "ph.d", "diploma"]
    education = next((term.upper() for term in education_terms if term in low), "Not detected")
    # Use anonymized IDs rather than extracting names for ranking.
    candidate_id = Path(filename).stem[:40]
    return {
        "candidate_id": candidate_id,
        "filename": filename,
        "raw_text": text,
        "skills": skills,
        "experience_years": experience,
        "education": education,
        "projects": []
    }
