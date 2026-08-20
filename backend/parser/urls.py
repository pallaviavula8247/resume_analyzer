from django.urls import path

from .views import (
    ResumeUploadView,
    ResumeListView,
    ResumeDetailView,
    ResumeAnalyzeView,
)

from analyzer.views import ResumeAnalysisView
from jobs.views import ResumeJobsView


urlpatterns = [

    # Upload resume
    path(
        "upload/",
        ResumeUploadView.as_view(),
        name="resume-upload",
    ),

    # List user's resumes
    path(
        "",
        ResumeListView.as_view(),
        name="resume-list",
    ),

    # Get specific resume
    path(
        "<int:pk>/",
        ResumeDetailView.as_view(),
        name="resume-detail",
    ),

    # Analyze specific resume
    path(
        "<int:pk>/analyze/",
        ResumeAnalyzeView.as_view(),
        name="resume-analyze",
    ),

    # Get analysis results
    path(
        "<int:pk>/analysis/",
        ResumeAnalysisView.as_view(),
        name="resume-analysis",
    ),

    # Get jobs matched to specific resume
    path(
        "<int:pk>/jobs/",
        ResumeJobsView.as_view(),
        name="resume-jobs",
    ),
]