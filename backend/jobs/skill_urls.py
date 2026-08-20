from django.urls import path
from .views import JobListView, JobDetailView
from .skill_views import SkillListView

urlpatterns = [
    path("", SkillListView.as_view()),
]
