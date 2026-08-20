from django.db import models

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=50, blank=True)
    related_jobs = models.JSONField(default=list, blank=True)
    related_skills = models.JSONField(default=list, blank=True)
    learning_priority = models.CharField(max_length=30, default="Medium")

    def __str__(self):
        return self.name

class Job(models.Model):
    title = models.CharField(max_length=150, unique=True)
    description = models.TextField()
    required_skills = models.JSONField(default=list)
    preferred_skills = models.JSONField(default=list)
    education = models.JSONField(default=list, blank=True)
    experience_level = models.CharField(max_length=80, default="Entry Level")
    experience_years = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
