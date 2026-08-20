from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [("parser", "0001_initial")]
    operations = [
        migrations.CreateModel(
            name="ResumeAnalysis",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("ats_score", models.FloatField(default=0)),
                ("score_breakdown", models.JSONField(default=dict)),
                ("strengths", models.JSONField(default=list)),
                ("weaknesses", models.JSONField(default=list)),
                ("missing_skills", models.JSONField(default=list)),
                ("created_at", models.DateTimeField(auto_now=True)),
                ("resume", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="analysis", to="parser.resume")),
            ],
        ),
    ]
