from .scoring import score_resume
from ..models import ResumeAnalysis
from jobs.models import Job

def analyze_resume(resume):
    score, breakdown = score_resume(resume)

    skills = {s.lower() for s in resume.skills}
    strengths = []
    weaknesses = []

    if len(skills) >= 8:
        strengths.append(f"Broad technical skill coverage with {len(skills)} detected skills.")
    elif skills:
        strengths.append(f"Clear technical profile with {len(skills)} detected skills.")

    if len(resume.projects) >= 2:
        strengths.append(f"{len(resume.projects)} projects provide evidence of practical work.")
    if resume.experience:
        strengths.append(f"{len(resume.experience)} experience record(s) provide professional context.")
    if resume.education:
        strengths.append("Education information was detected and can be used in job matching.")
    if resume.certifications:
        strengths.append("Certifications were detected and can strengthen role relevance.")

    if not resume.phone:
        weaknesses.append("Phone number was not detected.")
    if not resume.experience:
        weaknesses.append("No experience section was detected; projects can help demonstrate practical ability.")
    if len(skills) < 5:
        weaknesses.append("The extracted technical skill set is relatively small; adding relevant, evidenced skills may improve matching.")
    if not resume.projects:
        weaknesses.append("No project section was detected.")

    job_requirements = set()
    for job in Job.objects.all():
        job_requirements.update(s.lower() for s in job.required_skills)
    missing = sorted(job_requirements - skills)[:15]

    analysis, _ = ResumeAnalysis.objects.update_or_create(
        resume=resume,
        defaults={
            "ats_score": score,
            "score_breakdown": breakdown,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "missing_skills": missing,
        },
    )

    return {
        "success": True,
        "resume_id": resume.id,
        "ats_score": score,
        "score_breakdown": breakdown,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "missing_skills": missing,
    }
