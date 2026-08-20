from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

from parser.models import Resume
from .models import ResumeAnalysis

class ResumeAnalysisView(APIView):
    def get(self, request, pk):
        resume = get_object_or_404(Resume, pk=pk, user=request.user)
        analysis = getattr(resume, "analysis", None)
        if not analysis:
            from .services.analysis import analyze_resume
            data = analyze_resume(resume)
        else:
            data = {
                "success": True,
                "resume_id": resume.id,
                "ats_score": analysis.ats_score,
                "score_breakdown": analysis.score_breakdown,
                "strengths": analysis.strengths,
                "weaknesses": analysis.weaknesses,
                "missing_skills": analysis.missing_skills,
            }
        return Response(data)
