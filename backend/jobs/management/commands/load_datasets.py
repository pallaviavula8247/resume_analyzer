import json
from pathlib import Path
from django.core.management.base import BaseCommand
from jobs.models import Job, Skill

class Command(BaseCommand):
    help = "Load jobs and skills from JSON datasets."

    def handle(self, *args, **options):
        base = Path(__file__).resolve().parents[3] / "datasets"

        jobs = json.loads((base / "jobs.json").read_text(encoding="utf-8"))
        skills = json.loads((base / "skills.json").read_text(encoding="utf-8"))

        for item in jobs:
            Job.objects.update_or_create(
                title=item["job_title"],
                defaults={
                    "description": item["description"],
                    "required_skills": item.get("required_skills", []),
                    "preferred_skills": item.get("preferred_skills", []),
                    "education": item.get("education", []),
                    "experience_level": item.get("experience_level", "Entry Level"),
                    "experience_years": item.get("experience_years", 0),
                },
            )

        for item in skills:
            Skill.objects.update_or_create(
                name=item["skill"],
                defaults={
                    "category": item.get("category", "General"),
                    "related_jobs": item.get("related_jobs", []),
                    "difficulty": item.get("difficulty", "Intermediate"),
                    "related_skills": item.get("related_skills", []),
                    "learning_priority": item.get("learning_priority", "Medium"),
                },
            )

        self.stdout.write(self.style.SUCCESS(
            f"Loaded {len(jobs)} jobs and {len(skills)} skills."
        ))
