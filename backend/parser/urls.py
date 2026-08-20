from django.urls import path
from .views import ResumeUploadView, ResumeListView, ResumeDetailView, ResumeAnalyzeView
from analyzer.views import ResumeAnalysisView
from jobs.views import ResumeJobsView

urlpatterns = [
    path("upload/", ResumeUploadView.as_view()),
    path("", ResumeListView.as_view()),
    path("<int:pk>/", ResumeDetailView.as_view()),
    path("<int:pk>/analyze/", ResumeAnalyzeView.as_view()),
    path("<int:pk>/analysis/", ResumeAnalysisView.as_view()),
    path("<int:pk>/jobs/", ResumeJobsView.as_view()),
]
