from rest_framework import serializers
from .models import Resume

class ResumeUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ("id", "resume_file", "uploaded_at")

    def validate_resume_file(self, value):
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("PDF must be 5 MB or smaller.")
        if not value.name.lower().endswith(".pdf"):
            raise serializers.ValidationError("Only PDF resumes are supported.")
        if value.content_type not in ("application/pdf", "application/octet-stream"):
            raise serializers.ValidationError("Uploaded file must be a PDF.")
        return value

class ResumeDetailSerializer(serializers.ModelSerializer):
    structured_data = serializers.SerializerMethodField()

    class Meta:
        model = Resume
        fields = (
            "id", "uploaded_at", "parse_status", "parse_error",
            "full_name", "email", "phone", "location",
            "linkedin", "github", "portfolio",
            "skills", "education", "experience", "projects",
            "certifications", "languages", "achievements",
            "structured_data",
        )

    def get_structured_data(self, obj):
        return {
            "personal_info": {
                "name": obj.full_name,
                "email": obj.email,
                "phone": obj.phone,
                "location": obj.location,
                "linkedin": obj.linkedin,
                "github": obj.github,
                "portfolio": obj.portfolio,
            },
            "skills": obj.skills,
            "education": obj.education,
            "experience": obj.experience,
            "projects": obj.projects,
            "certifications": obj.certifications,
            "languages": obj.languages,
            "achievements": obj.achievements,
        }
