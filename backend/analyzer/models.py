from django.db import models
from parser.models import Resume

class ResumeAnalysis(models.Model):
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE, related_name="analysis")
    ats_score = models.FloatField(default=0)
    score_breakdown = models.JSONField(default=dict)
    strengths = models.JSONField(default=list)
    weaknesses = models.JSONField(default=list)
    missing_skills = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Analysis for Resume #{self.resume_id}"
