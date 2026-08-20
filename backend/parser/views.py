from django.conf import settings
from django.db import transaction
from rest_framework import generics, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Resume
from .serializers import ResumeUploadSerializer, ResumeDetailSerializer
from .services import extract_text_from_pdf, parse_resume

class ResumeUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ResumeUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        resume = serializer.save(user=request.user)
        try:
            text = extract_text_from_pdf(resume.resume_file.path)
            parsed = parse_resume(text)

            with transaction.atomic():
                resume.extracted_text = text
                info = parsed["personal_info"]
                resume.full_name = info.get("name")
                resume.email = info.get("email")
                resume.phone = info.get("phone")
                resume.linkedin = info.get("linkedin")
                resume.github = info.get("github")
                resume.portfolio = info.get("portfolio")
                resume.skills = parsed["skills"]
                resume.education = parsed["education"]
                resume.experience = parsed["experience"]
                resume.projects = parsed["projects"]
                resume.certifications = parsed["certifications"]
                resume.languages = parsed["languages"]
                resume.achievements = parsed["achievements"]
                resume.parse_status = "processed"
                resume.parse_error = None
                resume.save()

            return Response({
                "success": True,
                "resume_id": resume.id,
                "message": "Resume uploaded and processed successfully",
            }, status=status.HTTP_201_CREATED)
        except Exception as exc:
            resume.parse_status = "failed"
            resume.parse_error = str(exc)
            resume.save(update_fields=["parse_status", "parse_error"])
            resume.delete()
            return Response({
                "success": False,
                "message": str(exc),
            }, status=status.HTTP_400_BAD_REQUEST)

class ResumeListView(generics.ListAPIView):
    serializer_class = ResumeDetailSerializer

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

class ResumeDetailView(generics.RetrieveAPIView):
    serializer_class = ResumeDetailSerializer

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

class ResumeAnalyzeView(APIView):
    def post(self, request, pk):
        resume = generics.get_object_or_404(Resume, pk=pk, user=request.user)
        from analyzer.services.analysis import analyze_resume
        result = analyze_resume(resume)
        return Response(result)
