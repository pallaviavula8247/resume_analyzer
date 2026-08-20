ATS_WEIGHTS = {
    "contact_completeness": 15,
    "skills": 25,
    "education": 15,
    "experience": 20,
    "projects": 15,
    "certifications": 5,
    "achievements": 5,
}

def score_resume(resume):
    checks = {
        "contact_completeness": sum(bool(x) for x in [
            resume.full_name, resume.email, resume.phone
        ]) / 3,
        "skills": min(len(resume.skills) / 10, 1),
        "education": min(len(resume.education) / 2, 1),
        "experience": min(len(resume.experience) / 2, 1),
        "projects": min(len(resume.projects) / 3, 1),
        "certifications": 1 if resume.certifications else 0,
        "achievements": 1 if resume.achievements else 0,
    }
    breakdown = {
        key: round(checks[key] * weight, 2)
        for key, weight in ATS_WEIGHTS.items()
    }
    total = round(sum(breakdown.values()), 2)
    return total, breakdown
