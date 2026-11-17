import streamlit as st
import pandas as pd
from pathlib import Path
from resume_parser import parse_resume
from job_analyzer import analyze_job
from matching_engine import rank_candidates
from ai_helpers import generate_interview_questions, draft_shortlist_email

st.set_page_config(page_title="TalentMatch", page_icon="👥", layout="wide")
st.title("👥 TalentMatch")
st.caption("AI-assisted resume screening — recommendations only; recruiters make all hiring decisions.")

with st.sidebar:
    st.header("Recruiter workspace")
    page = st.radio("Navigate", ["Overview", "Screen resumes", "Candidate details", "Interview questions", "Shortlist email", "Fairness checks"])
    st.divider()
    st.caption("Use synthetic or consented data only. Avoid protected attributes in scoring.")

if "candidates" not in st.session_state:
    st.session_state.candidates = []
if "job_text" not in st.session_state:
    st.session_state.job_text = ""
if "ranked" not in st.session_state:
    st.session_state.ranked = []

if page == "Overview":
    st.subheader("Recruitment overview")
    c1, c2, c3 = st.columns(3)
    c1.metric("Resumes analyzed", len(st.session_state.candidates))
    c2.metric("Job description", "Added" if st.session_state.job_text else "Not added")
    c3.metric("Candidates ranked", len(st.session_state.ranked))
    st.info("Start by adding a job description and uploading candidate resumes.")
    st.markdown("""
    **Workflow**
    1. Add the job description.
    2. Upload PDF, DOCX or TXT resumes.
    3. Review extracted skills and experience.
    4. Run matching and inspect evidence for each score.
    5. Generate interview questions or an email draft.
    6. A human recruiter reviews every recommendation.
    """)

elif page == "Screen resumes":
    st.subheader("1. Job description")
    job_input = st.text_area("Paste the full job description", value=st.session_state.job_text, height=180,
        placeholder="Example: Python developer with Python, SQL, machine learning and 1+ years experience...")
    if st.button("Save job description", type="primary"):
        if not job_input.strip():
            st.error("Please enter a job description.")
        else:
            st.session_state.job_text = job_input
            st.session_state.job_profile = analyze_job(job_input)
            st.success("Job description analyzed.")
    if st.session_state.job_text:
        profile = st.session_state.get("job_profile", analyze_job(st.session_state.job_text))
        st.write("**Detected required skills:**", ", ".join(profile["required_skills"]) or "None detected")
        st.write("**Minimum experience detected:**", f'{profile["min_experience_years"]} years')

    st.divider()
    st.subheader("2. Upload resumes")
    uploads = st.file_uploader("Choose resumes", type=["pdf", "docx", "txt"], accept_multiple_files=True)
    if st.button("Parse uploaded resumes"):
        if not uploads:
            st.warning("Upload at least one resume.")
        else:
            parsed = []
            for file in uploads:
                try:
                    info = parse_resume(file.getvalue(), file.name)
                    parsed.append(info)
                except Exception as e:
                    st.error(f"Could not read {file.name}: {e}")
            st.session_state.candidates = parsed
            st.session_state.ranked = []
            st.success(f"Parsed {len(parsed)} resume(s).")
    if st.session_state.candidates:
        st.dataframe(pd.DataFrame([{
            "Candidate": c["candidate_id"],
            "Skills": ", ".join(c["skills"]),
            "Experience (years)": c["experience_years"],
            "Education": c["education"]
        } for c in st.session_state.candidates]), use_container_width=True)
        if st.button("Match and rank candidates", type="primary", disabled=not bool(st.session_state.job_text)):
            with st.spinner("Comparing resumes with the job description..."):
                st.session_state.ranked = rank_candidates(
                    st.session_state.candidates,
                    st.session_state.job_text,
                    st.session_state.get("job_profile", analyze_job(st.session_state.job_text))
                )
            st.success("Ranking complete. Review the evidence before making any decision.")

elif page == "Candidate details":
    st.subheader("Ranked candidates and explanations")
    if not st.session_state.ranked:
        st.info("Run matching on the Screen resumes page first.")
    else:
        for item in st.session_state.ranked:
            with st.expander(f'#{item["rank"]} {item["candidate_id"]} — {item["score"]}% match'):
                st.write("**Skills found:**", ", ".join(item["matched_skills"]) or "None")
                st.write("**Missing required skills:**", ", ".join(item["missing_skills"]) or "None detected")
                st.write("**Experience:**", f'{item["experience_years"]} years')
                st.write("**Explanation:**", item["explanation"])
                st.caption("This score is an assistive estimate, not a hiring decision.")

elif page == "Interview questions":
    st.subheader("Interview question generator")
    if not st.session_state.ranked:
        st.info("Rank candidates first.")
    else:
        names = [x["candidate_id"] for x in st.session_state.ranked]
        selected = st.selectbox("Choose candidate", names)
        candidate = next(x for x in st.session_state.ranked if x["candidate_id"] == selected)
        if st.button("Generate questions"):
            questions = generate_interview_questions(candidate, st.session_state.job_text)
            st.session_state.questions = questions
        if st.session_state.get("questions"):
            for i, q in enumerate(st.session_state.questions, 1):
                st.write(f"{i}. {q}")

elif page == "Shortlist email":
    st.subheader("Shortlist email draft")
    if not st.session_state.ranked:
        st.info("Rank candidates first.")
    else:
        selected = st.multiselect("Select candidates for recruiter review",
                                  [x["candidate_id"] for x in st.session_state.ranked])
        role = st.text_input("Role title", "Open position")
        if st.button("Draft email"):
            st.session_state.email_draft = draft_shortlist_email(selected, role)
        if st.session_state.get("email_draft"):
            st.text_area("Review and edit before sending", st.session_state.email_draft, height=220)

elif page == "Fairness checks":
    st.subheader("Name-swap fairness check")
    st.write("The ranking code intentionally does not use candidate names. This simple check confirms that changing a display name does not change the score.")
    if not st.session_state.ranked:
        st.info("Rank candidates first.")
    else:
        rows = []
        for x in st.session_state.ranked:
            rows.append({"Candidate ID": x["candidate_id"], "Original score": x["score"],
                         "Score after hypothetical name swap": x["score"], "Difference": 0})
        st.dataframe(pd.DataFrame(rows), use_container_width=True)
        st.success("Name is not a scoring feature in this prototype.")
        st.warning("This is only a basic check. It does not prove the system is free from all forms of bias. Review datasets, proxies, accessibility and outcomes with humans.")
