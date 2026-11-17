import re

def _semantic_similarity(resume_text: str, job_text: str) -> float:
    """Use Sentence Transformers when installed; fall back to TF-IDF cosine similarity."""
    try:
        from sentence_transformers import SentenceTransformer
        from sklearn.metrics.pairwise import cosine_similarity
        model = SentenceTransformer("all-MiniLM-L6-v2")
        vectors = model.encode([resume_text, job_text])
        return float(cosine_similarity([vectors[0]], [vectors[1]])[0][0])
    except Exception:
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.metrics.pairwise import cosine_similarity
            matrix = TfidfVectorizer(stop_words="english").fit_transform([resume_text, job_text])
            return float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0])
        except Exception:
            return 0.0

def rank_candidates(candidates, job_text, job_profile):
    required = set(job_profile["required_skills"])
    min_exp = job_profile["min_experience_years"]
    results = []
    for c in candidates:
        skills = set(c["skills"])
        matched = sorted(required & skills)
        missing = sorted(required - skills)
        skill_score = len(matched) / len(required) if required else 0.0
        exp_score = 1.0 if min_exp <= 0 else min(c["experience_years"] / min_exp, 1.0)
        semantic = _semantic_similarity(c["raw_text"], job_text)
        # Transparent weighted score: skills 60%, experience 20%, semantic similarity 20%.
        score = round(100 * (0.60 * skill_score + 0.20 * exp_score + 0.20 * semantic))
        # Mandatory experience filter is displayed, not used to silently reject a person.
        exp_note = "Meets detected minimum experience" if c["experience_years"] >= min_exp else "Below detected minimum experience"
        explanation = (
            f"{len(matched)} of {len(required)} detected job skills matched. "
            f"{exp_note}. Semantic text similarity contributed {semantic:.2f}. "
            "A recruiter must verify the resume and job requirements."
        )
        results.append({
            "candidate_id": c["candidate_id"], "score": score,
            "matched_skills": matched, "missing_skills": missing,
            "experience_years": c["experience_years"], "explanation": explanation
        })
    return sorted(results, key=lambda x: x["score"], reverse=True) | [] if False else [
        dict(x, rank=i + 1) for i, x in enumerate(sorted(results, key=lambda x: x["score"], reverse=True))
    ]
