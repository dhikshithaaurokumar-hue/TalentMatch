def _gemini_generate(prompt: str):
    """Optional Gemini integration. Set GOOGLE_API_KEY to enable it."""
    import os
    key = os.getenv("GOOGLE_API_KEY")
    if not key:
        return None
    try:
        from google import genai
        client = genai.Client(api_key=key)
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        return response.text
    except Exception:
        return None

def generate_interview_questions(candidate: dict, job_text: str):
    prompt = f"""Create 6 fair, job-related interview questions. Use only the candidate's listed skills and this job description.
Candidate skills: {candidate.get('matched_skills', [])}
Job description: {job_text}
Return a numbered list. Do not ask about age, gender, religion, caste, disability, family or other protected traits."""
    answer = _gemini_generate(prompt)
    if answer:
        return [line.strip("0123456789. -") for line in answer.splitlines() if line.strip()][:8]
    skills = candidate.get("matched_skills", [])[:5]
    if not skills:
        skills = ["the core responsibilities of this role"]
    return [f"Can you explain a project or task where you used {skill}?" for skill in skills] + [
        "Describe how you approach learning a new technical concept."
    ]

def draft_shortlist_email(candidate_ids, role):
    names = "\n".join(f"- {name}" for name in candidate_ids) or "- [Add candidate names]"
    prompt = f"Draft a concise internal recruiter email asking for human review of these candidates for {role}:\n{names}"
    answer = _gemini_generate(prompt)
    if answer:
        return answer
    return f"""Subject: Candidate shortlist for {role}

Hi team,

Please review the following candidates for the {role} position:

{names}

These are AI-generated recommendations only. Please verify each resume against the job criteria and make all interview and hiring decisions through the normal human review process.

Regards,
Recruitment Team
"""
