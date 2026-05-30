import re
from pathlib import Path

from flask import Flask, jsonify, request, send_file
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


app = Flask(__name__)
INDEX_FILE = Path(__file__).resolve().parent / "index.html"


SKILLS = {
    "python",
    "java",
    "javascript",
    "react",
    "flask",
    "sql",
    "postgresql",
    "excel",
    "power bi",
    "tableau",
    "machine learning",
    "nlp",
    "pandas",
    "numpy",
    "scikit-learn",
    "aws",
    "docker",
    "kubernetes",
    "git",
    "ci/cd",
    "rest api",
    "linux",
}


JOBS = [
    {
        "title": "Data Analyst Intern",
        "company": "InsightWorks",
        "location": "Remote",
        "description": "Analyze business data, build dashboards, clean datasets, and communicate insights.",
        "required_skills": ["sql", "excel", "python", "power bi", "tableau"],
    },
    {
        "title": "Junior Backend Developer",
        "company": "CloudNest",
        "location": "Bengaluru",
        "description": "Build REST APIs, work with databases, write backend services, and deploy applications.",
        "required_skills": ["python", "flask", "postgresql", "rest api", "docker", "git"],
    },
    {
        "title": "Machine Learning Intern",
        "company": "ModelMind",
        "location": "Hyderabad",
        "description": "Develop ML models, evaluate experiments, process data, and support NLP projects.",
        "required_skills": ["python", "machine learning", "pandas", "numpy", "scikit-learn", "nlp"],
    },
    {
        "title": "Cloud DevOps Trainee",
        "company": "DeployHub",
        "location": "Pune",
        "description": "Support cloud deployments, containers, CI/CD pipelines, and infrastructure automation.",
        "required_skills": ["aws", "docker", "kubernetes", "linux", "ci/cd", "git"],
    },
]


COURSES = {
    "sql": {
        "title": "SQL for Data Analysis",
        "provider": "Coursera / freeCodeCamp",
        "project": "Build a job-market analytics SQL dashboard",
    },
    "power bi": {
        "title": "Power BI Dashboarding",
        "provider": "Microsoft Learn",
        "project": "Create an employability KPI dashboard",
    },
    "tableau": {
        "title": "Tableau Fundamentals",
        "provider": "Tableau Training",
        "project": "Visualize internship trends by skill and location",
    },
    "flask": {
        "title": "Flask REST API Development",
        "provider": "Real Python / YouTube",
        "project": "Build a resume analysis API",
    },
    "postgresql": {
        "title": "PostgreSQL for Developers",
        "provider": "PostgreSQL Tutorial",
        "project": "Design a career platform database",
    },
    "docker": {
        "title": "Docker Essentials",
        "provider": "Docker Docs",
        "project": "Containerize the Flask career API",
    },
    "machine learning": {
        "title": "Applied Machine Learning",
        "provider": "Kaggle Learn",
        "project": "Train a job recommendation model",
    },
    "pandas": {
        "title": "Pandas Data Cleaning",
        "provider": "Kaggle Learn",
        "project": "Clean job description datasets",
    },
    "numpy": {
        "title": "NumPy Fundamentals",
        "provider": "Kaggle Learn",
        "project": "Create vectorized scoring functions",
    },
    "scikit-learn": {
        "title": "scikit-learn Model Building",
        "provider": "Official scikit-learn Tutorials",
        "project": "Build a resume-job matching baseline",
    },
    "nlp": {
        "title": "NLP with Python",
        "provider": "Hugging Face Course",
        "project": "Extract skills from job descriptions",
    },
    "aws": {
        "title": "AWS Cloud Practitioner Basics",
        "provider": "AWS Skill Builder",
        "project": "Deploy the career intelligence backend",
    },
    "kubernetes": {
        "title": "Kubernetes Basics",
        "provider": "Kubernetes Docs",
        "project": "Deploy API services to a local cluster",
    },
    "linux": {
        "title": "Linux Command Line Basics",
        "provider": "freeCodeCamp",
        "project": "Automate server setup tasks",
    },
    "ci/cd": {
        "title": "CI/CD Pipeline Fundamentals",
        "provider": "GitHub Actions Docs",
        "project": "Create a test and deploy workflow",
    },
    "rest api": {
        "title": "REST API Design",
        "provider": "Postman Academy",
        "project": "Document the career platform API",
    },
    "git": {
        "title": "Git and GitHub Essentials",
        "provider": "GitHub Skills",
        "project": "Publish your platform source code",
    },
}


def normalize_text(text):
    return re.sub(r"\s+", " ", text.lower()).strip()


def extract_skills(text):
    normalized = normalize_text(text)
    detected = []

    for skill in sorted(SKILLS):
        pattern = r"(^|[^a-z0-9+#.])" + re.escape(skill) + r"([^a-z0-9+#.]|$)"
        if re.search(pattern, normalized):
            detected.append(skill)

    return detected


def score_resume(text, detected_skills):
    normalized = text.lower()
    score = 40
    feedback = []

    sections = {
        "summary": ["summary", "profile", "objective"],
        "experience": ["experience", "work history", "internship"],
        "education": ["education", "degree", "university", "college"],
        "skills": ["skills", "technical skills", "tools"],
        "projects": ["projects", "portfolio"],
    }

    for section, aliases in sections.items():
        if any(alias in normalized for alias in aliases):
            score += 7
        else:
            feedback.append(f"Add a clear {section} section.")

    if len(detected_skills) >= 8:
        score += 15
    elif len(detected_skills) >= 4:
        score += 8
    else:
        feedback.append("Add more role-relevant technical skills.")

    action_verbs = ["built", "created", "developed", "designed", "improved", "analyzed", "automated", "deployed"]
    action_count = sum(1 for verb in action_verbs if verb in normalized)
    if action_count >= 4:
        score += 10
    elif action_count >= 2:
        score += 5
    else:
        feedback.append("Use stronger action verbs in project and experience bullets.")

    if re.search(r"\d+%|\d+\+|\d+\s*(users|students|projects|hours|days)", normalized):
        score += 10
    else:
        feedback.append("Add measurable impact such as percentages, counts, or time saved.")

    if len(text.split()) < 120:
        score -= 8
        feedback.append("Resume text looks short. Add more detail about projects and achievements.")

    return {"score": max(0, min(score, 100)), "feedback": feedback[:5]}


def match_jobs(resume_text, detected_skills):
    documents = [resume_text] + [
        f"{job['title']} {job['description']} {' '.join(job['required_skills'])}"
        for job in JOBS
    ]
    vectors = TfidfVectorizer(stop_words="english", ngram_range=(1, 2)).fit_transform(documents)
    similarities = cosine_similarity(vectors[0:1], vectors[1:]).flatten()
    detected = set(detected_skills)
    matches = []

    for index, job in enumerate(JOBS):
        required = set(job["required_skills"])
        matched_skills = sorted(required.intersection(detected))
        missing_skills = sorted(required.difference(detected))
        skill_score = len(matched_skills) / max(len(required), 1)
        final_score = round((float(similarities[index]) * 0.55 + skill_score * 0.45) * 100)

        matches.append(
            {
                "title": job["title"],
                "company": job["company"],
                "location": job["location"],
                "match_score": final_score,
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
            }
        )

    return sorted(matches, key=lambda item: item["match_score"], reverse=True)


def recommend_courses(job_matches, detected_skills):
    detected = set(detected_skills)
    missing_skills = []

    for job in job_matches[:3]:
        for skill in job["missing_skills"]:
            if skill not in detected and skill not in missing_skills:
                missing_skills.append(skill)

    return [
        {"skill": skill, **COURSES[skill]}
        for skill in missing_skills[:6]
        if skill in COURSES
    ]


@app.get("/")
def home():
    return send_file(INDEX_FILE)


@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/api/analyze")
def analyze_resume():
    payload = request.get_json(silent=True) or {}
    resume_text = payload.get("resume_text", "").strip()

    if not resume_text:
        return jsonify({"error": "Please paste resume text first."}), 400

    detected_skills = extract_skills(resume_text)
    ats_result = score_resume(resume_text, detected_skills)
    job_matches = match_jobs(resume_text, detected_skills)

    return jsonify(
        {
            "ats_score": ats_result["score"],
            "ats_feedback": ats_result["feedback"],
            "detected_skills": detected_skills,
            "job_matches": job_matches[:5],
            "learning_recommendations": recommend_courses(job_matches, detected_skills),
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
