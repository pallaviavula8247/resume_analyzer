from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

WEIGHTS = {
    "required_skills": 50,
    "preferred_skills": 10,
    "education": 15,
    "experience": 15,
    "projects": 10,
}

def norm(values):
    return {str(v).strip().lower() for v in (values or []) if str(v).strip()}

def skill_score(candidate, required):
    required = norm(required)
    candidate = norm(candidate)
    if not required:
        return 100.0, [], []
    matched = sorted(required & candidate)
    missing = sorted(required - candidate)
    return round(len(matched) / len(required) * 100, 2), matched, missing

def education_score(resume, job):
    if not job.education:
        return 100.0
    text = " ".join(str(x) for x in resume.education).lower()
    return 100.0 if any(str(x).lower() in text for x in job.education) else 0.0

def experience_score(resume, job):
    if job.experience_years <= 0:
        return 100.0
    years = 0
    for item in resume.experience:
        duration = str(item.get("duration") or "")
        found = [int(x) for x in __import__("re").findall(r"(?:19|20)\d{2}", duration)]
        if len(found) >= 2:
            years += max(0, found[-1] - found[0])
    return min(100.0, years / job.experience_years * 100)

def project_score(resume, job):
    if not resume.projects:
        return 0.0
    project_text = " ".join(
        f"{p.get('title','')} {p.get('description','')} {' '.join(p.get('technologies', []))}"
        for p in resume.projects
    )
    job_text = f"{job.title} {job.description} {' '.join(job.required_skills)}"
    try:
        vectorizer = TfidfVectorizer(stop_words="english")
        matrix = vectorizer.fit_transform([project_text, job_text])
        return round(float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0]) * 100, 2)
    except ValueError:
        return 0.0

def match_resume_to_job(resume, job):
    required, matched, missing = skill_score(resume.skills, job.required_skills)
    preferred, _, _ = skill_score(resume.skills, job.preferred_skills)
    education = education_score(resume, job)
    experience = experience_score(resume, job)
    projects = project_score(resume, job)

    final = round(
        required * 0.50 +
        preferred * 0.10 +
        education * 0.15 +
        experience * 0.15 +
        projects * 0.10,
        2,
    )

    reasons = []
    if matched:
        reasons.append(f"Matched required skills: {', '.join(matched[:6])}.")
    if education == 100:
        reasons.append("Education information is relevant to the role.")
    if experience >= 75:
        reasons.append("Experience evidence is reasonably aligned with the role.")
    if projects >= 50:
        reasons.append("Project descriptions show meaningful relevance to this role.")

    return {
        "job_id": job.id,
        "job_title": job.title,
        "match_percentage": final,
        "matched_skills": matched,
        "missing_skills": missing,
        "preferred_skills_matched": sorted(norm(resume.skills) & norm(job.preferred_skills)),
        "score_breakdown": {
            "required_skills": required,
            "preferred_skills": preferred,
            "education": education,
            "experience": experience,
            "projects": projects,
        },
        "why_recommended": reasons or ["The role has some measurable overlap with the uploaded resume."],
    }
