from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()

try:
    admin.site.register(User)
except admin.sites.AlreadyRegistered:
    pass