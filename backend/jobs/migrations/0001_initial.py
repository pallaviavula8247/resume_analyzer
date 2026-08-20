from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    operations = [
        migrations.CreateModel(
            name="Job",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=150, unique=True)),
                ("description", models.TextField()),
                ("required_skills", models.JSONField(default=list)),
                ("preferred_skills", models.JSONField(default=list)),
                ("education", models.JSONField(blank=True, default=list)),
                ("experience_level", models.CharField(default="Entry Level", max_length=80)),
                ("experience_years", models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="Skill",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True)),
                ("category", models.CharField(max_length=100)),
                ("difficulty", models.CharField(blank=True, max_length=50)),
                ("related_jobs", models.JSONField(blank=True, default=list)),
                ("related_skills", models.JSONField(blank=True, default=list)),
                ("learning_priority", models.CharField(default="Medium", max_length=30)),
            ],
        ),
    ]
