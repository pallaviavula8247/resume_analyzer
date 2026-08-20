from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404

from parser.models import Resume
from .models import Job
from .serializers import JobSerializer
from .services.matching import match_resume_to_job

class JobListView(generics.ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

class JobDetailView(generics.RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

class ResumeJobsView(APIView):
    def get(self, request, pk):
        resume = get_object_or_404(Resume, pk=pk, user=request.user)
        results = [match_resume_to_job(resume, job) for job in Job.objects.all()]
        results.sort(key=lambda x: x["match_percentage"], reverse=True)
        return Response({
            "success": True,
            "resume_id": resume.id,
            "jobs": results,
        })
