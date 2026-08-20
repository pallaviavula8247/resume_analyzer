from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [("parser", "0001_initial")]
    operations = [
        migrations.CreateModel(
            name="RecommendationSnapshot",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("jobs", models.JSONField(default=list)),
                ("skills", models.JSONField(default=list)),
                ("created_at", models.DateTimeField(auto_now=True)),
                ("resume", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="recommendation_snapshot", to="parser.resume")),
            ],
        ),
    ]
