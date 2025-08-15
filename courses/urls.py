from django.urls import path
from .views import (
    CourseListView,
    CourseDetailView,
    CourseEnrollView,
    CourseUnenrollView,
)

app_name = "courses"

urlpatterns = [
    path("", CourseListView.as_view(), name="list"),
    path("<slug:slug>/", CourseDetailView.as_view(), name="detail"),

    # Enroll / Unenroll
    path("<slug:slug>/enroll/", CourseEnrollView.as_view(), name="enroll"),
    path("<slug:slug>/unenroll/", CourseUnenrollView.as_view(), name="unenroll"),
]

