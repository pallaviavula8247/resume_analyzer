from django.db import models
from parser.models import Resume

class RecommendationSnapshot(models.Model):
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE, related_name="recommendation_snapshot")
    jobs = models.JSONField(default=list)
    skills = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now=True)
