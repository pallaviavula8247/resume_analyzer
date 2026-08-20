from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from parser.models import Resume
from .services import build_recommendations

class RecommendationView(APIView):
    def get(self, request, pk):
        resume = get_object_or_404(Resume, pk=pk, user=request.user)
        return Response(build_recommendations(resume))
