# AI-Powered Career Intelligence Platform

This is an MVP starter system for an AI/ML career platform. It lets a user upload or paste resume text, extracts skills, scores ATS readiness, compares the resume with job roles, identifies skill gaps, and recommends learning paths.

## Features

- Resume text analysis
- Skill extraction
- ATS-style scoring
- Job matching
- Skill gap analysis
- Learning recommendations
- Flask REST API
- React frontend

## Project Structure

Simple same-directory version:

```text
app.py
index.html
requirements.txt
```

Earlier separated version:

```text
backend/
  app.py
  requirements.txt
  data/
    jobs.json
    courses.json
  services/
    ats.py
    extractors.py
    job_matcher.py
    recommendations.py
frontend/
  package.json
  index.html
  src/
    App.jsx
    main.jsx
    styles.css
```

## Run Combined App

The easiest version keeps frontend and backend in the same directory. No npm is needed.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open:

```text
http://localhost:5000
```

## Optional React Frontend

Use this only if Node.js and npm are installed.

```bash
cd frontend
npm install
npm run dev
```

React frontend runs at:

```text
http://localhost:5173
```

## API

### Analyze Resume

```http
POST /api/analyze
Content-Type: application/json

{
  "resume_text": "Python SQL Excel data analyst internship..."
}
```

### Response

```json
{
  "ats_score": 78,
  "detected_skills": ["python", "sql", "excel"],
  "job_matches": [],
  "learning_recommendations": []
}
```

## Next AI/ML Upgrades

1. Add PDF/DOCX resume parsing.
2. Replace keyword skill extraction with spaCy NER.
3. Add sentence-transformer embeddings for semantic job matching.
4. Store resumes and jobs in PostgreSQL.
5. Add Qdrant or Pinecone for vector search.
6. Add LLM-based resume rewriting.
7. Add authentication and student dashboards.
