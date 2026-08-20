from django.urls import path

from .views import (
    RegisterView,
    LoginView,
    ProfileView,
)


urlpatterns = [

    # Register
    path(
        "register/",
        RegisterView.as_view(),
        name="register",
    ),

    # Login
    path(
        "login/",
        LoginView.as_view(),
        name="login",
    ),

    # Current user profile
    path(
        "profile/",
        ProfileView.as_view(),
        name="profile",
    ),
]