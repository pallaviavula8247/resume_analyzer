from django.db import migrations, models
import django.db.models.deletion
import django.conf
from django.db import migrations, models
from django.conf import settings

class Migration(migrations.Migration):
    initial = True
    dependencies = [
    migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    operations = [
        migrations.CreateModel(
            name="Resume",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("resume_file", models.FileField(upload_to="resumes/%Y/%m/")),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
                ("extracted_text", models.TextField(blank=True, null=True)),
                ("full_name", models.CharField(blank=True, max_length=255, null=True)),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                ("phone", models.CharField(blank=True, max_length=50, null=True)),
                ("location", models.CharField(blank=True, max_length=255, null=True)),
                ("linkedin", models.URLField(blank=True, max_length=200, null=True)),
                ("github", models.URLField(blank=True, max_length=200, null=True)),
                ("portfolio", models.URLField(blank=True, max_length=200, null=True)),
                ("skills", models.JSONField(blank=True, default=list)),
                ("education", models.JSONField(blank=True, default=list)),
                ("experience", models.JSONField(blank=True, default=list)),
                ("projects", models.JSONField(blank=True, default=list)),
                ("certifications", models.JSONField(blank=True, default=list)),
                ("languages", models.JSONField(blank=True, default=list)),
                ("achievements", models.JSONField(blank=True, default=list)),
                ("parse_status", models.CharField(default="pending", max_length=30)),
                ("parse_error", models.TextField(blank=True, null=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="resumes", to=django.conf.settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-uploaded_at"]},
        ),
    ]
