from parser.models import Resume
from jobs.models import Job, Skill
from jobs.services.matching import match_resume_to_job

def build_recommendations(resume):
    job_results = [match_resume_to_job(resume, job) for job in Job.objects.all()]
    job_results.sort(key=lambda x: x["match_percentage"], reverse=True)
    top_jobs = job_results[:10]

    current = {s.lower() for s in resume.skills}
    counts = {}
    metadata = {}

    for result in top_jobs:
        job = Job.objects.get(pk=result["job_id"])
        for missing in result["missing_skills"]:
            key = missing.lower()
            counts[key] = counts.get(key, 0) + 1
            metadata[key] = {
                "skill": missing,
                "reason": f"{missing} is required by {job.title}, which has a {result['match_percentage']}% match with your resume.",
                "related_jobs": [job.title],
                "priority": "High" if counts[key] >= 2 else "Medium",
                "required_or_optional": "Required",
            }

    recommendations = list(metadata.values())
    recommendations.sort(key=lambda x: (x["priority"] != "High", x["skill"]))

    return {
        "success": True,
        "resume_id": resume.id,
        "top_jobs": top_jobs,
        "skill_recommendations": recommendations[:15],
    }
