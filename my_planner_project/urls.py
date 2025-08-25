"""Main URL configuration for the MyPlanner project."""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("planner.urls_html")),   # HTML views for the planner app
    path("api/", include("planner.urls")),    # API endpoints for the planner app
    path("api-auth/", include("rest_framework.urls")),  # Login/logout for API
    path("admin/", admin.site.urls),          # Django admin site
]