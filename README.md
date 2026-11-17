# TalentMatch — AI Resume Screening & Recruitment Assistant

A beginner-friendly Streamlit prototype that extracts resume text, detects skills, compares candidates with a job description, ranks them with transparent reasons, and drafts interview questions and shortlist emails.

## Important limitations
- This is a prototype, not a validated hiring product.
- Scores are approximate decision-support signals, not probabilities of job performance.
- The parser uses simple rules and can miss information or misread formats.
- The semantic score uses Sentence Transformers when available, with TF-IDF fallback.
- ChromaDB is listed as an optional next-step vector store; this starter version performs direct pairwise comparison rather than persisting a vector index.
- Human recruiters must verify all extracted information and make all hiring decisions.
- Use synthetic, dummy, or properly authorized data only. Do not upload sensitive personal data.

## Setup (Windows / VS Code)

1. Install Python 3.10 or newer.
2. Open this folder in VS Code.
3. Create a virtual environment:

   ```powershell
   py -m venv .venv
   .venv\\Scripts\\activate
   ```

4. Install packages:

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. Run:

   ```powershell
   streamlit run app.py
   ```

6. Your browser should open the TalentMatch dashboard.

## Optional Gemini setup

Set an environment variable before starting Streamlit:

```powershell
$env:GOOGLE_API_KEY="your_key_here"
streamlit run app.py
```

Without an API key, interview questions and email drafts use local templates.

## Suggested demo

1. Paste a job description requiring Python, SQL and machine learning.
2. Upload 3–5 synthetic resumes in PDF, DOCX or TXT format.
3. Parse resumes.
4. Run candidate matching.
5. Open Candidate details and review matched/missing skills and explanations.
6. Generate interview questions and an email draft.
7. Run the name-swap fairness demonstration.

## Suggested future improvements for the full project brief

- Generate at least 50 synthetic resumes and 5 job descriptions.
- Add a ChromaDB collection and persistent embedding search.
- Improve parsing with structured LLM extraction and validation.
- Add recruiter-defined must-have and preferred skills separately.
- Add at least 10 documented evaluation scenarios, including keyword stuffing, career gaps, unusual formats, and name swapping.
- Add audit logs, consent/privacy controls, accessibility review, and human approval workflow.
