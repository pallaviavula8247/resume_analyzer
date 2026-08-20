from django.urls import path
from .views import RecommendationView

urlpatterns = [
    path("resume/<int:pk>/", RecommendationView.as_view()),
]
