from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin

from django.urls import include, path

from django.views.generic import TemplateView

from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [

    # ========================================================
    # HEALTH CHECK
    # ========================================================

    path(
        "health/",
        __import__(
            "config.health",
            fromlist=["health"]
        ).health,
        name="health",
    ),


    # ========================================================
    # ADMIN
    # ========================================================

    path(
        "admin/",
        admin.site.urls,
    ),


    # ========================================================
    # AUTHENTICATION
    # ========================================================

    path(
        "api/auth/",
        include("users.urls"),
    ),


    # ========================================================
    # JWT TOKEN REFRESH
    # ========================================================

    path(
        "api/auth/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),


    # ========================================================
    # RESUME APIs
    # ========================================================

    path(
        "api/resumes/",
        include("parser.urls"),
    ),


    # ========================================================
    # JOB APIs
    # ========================================================

    path(
        "api/jobs/",
        include("jobs.urls"),
    ),


    # ========================================================
    # SKILLS APIs
    # ========================================================

    path(
        "api/skills/",
        include("jobs.skill_urls"),
    ),


    # ========================================================
    # RECOMMENDATION APIs
    # ========================================================

    path(
        "api/recommendations/",
        include("recommendations.urls"),
    ),


    # ========================================================
    # FRONTEND PAGES
    # ========================================================

    path(
        "",
        TemplateView.as_view(
            template_name="index.html"
        ),
        name="home",
    ),

    path(
        "login/",
        TemplateView.as_view(
            template_name="login.html"
        ),
        name="login-page",
    ),

    path(
        "register/",
        TemplateView.as_view(
            template_name="register.html"
        ),
        name="register-page",
    ),

    path(
        "dashboard/",
        TemplateView.as_view(
            template_name="dashboard.html"
        ),
        name="dashboard-page",
    ),

    path(
        "upload/",
        TemplateView.as_view(
            template_name="upload.html"
        ),
        name="upload-page",
    ),

    path(
        "analysis/",
        TemplateView.as_view(
            template_name="analysis.html"
        ),
        name="analysis-page",
    ),

    path(
        "jobs/",
        TemplateView.as_view(
            template_name="jobs.html"
        ),
        name="jobs-page",
    ),

    path(
        "recommendations/",
        TemplateView.as_view(
            template_name="recommendations.html"
        ),
        name="recommendations-page",
    ),
]


# ============================================================
# MEDIA FILES
# DEVELOPMENT ONLY
# ============================================================

if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )