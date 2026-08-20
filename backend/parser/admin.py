from django.contrib import admin
from .models import Resume

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "uploaded_at", "parse_status")
    search_fields = ("user__username", "full_name", "email")
