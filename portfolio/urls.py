from django.urls import path
from django.views.generic import RedirectView
from .views import (
    MyProjectsListView, ProjectDetailView, ProjectCreateView,
    ProjectUpdateView, ProjectDeleteView, ReviewCreateView,
    ReviewUpdateView, ReviewDeleteView,   # NEW
)

app_name = "portfolio"

urlpatterns = [
    path("", MyProjectsListView.as_view(), name="projects"),

    # keep old /my/ link working
    path(
        "my/",
        RedirectView.as_view(pattern_name="portfolio:projects", permanent=False),
        name="my",
    ),

    path("create/", ProjectCreateView.as_view(), name="create"),
    path("<int:pk>/", ProjectDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", ProjectUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", ProjectDeleteView.as_view(), name="delete"),

    # reviews
    path("<int:project_pk>/reviews/add/", ReviewCreateView.as_view(), name="review_create"),
    path("reviews/<int:pk>/edit/", ReviewUpdateView.as_view(), name="review_edit"),     # NEW
    path("reviews/<int:pk>/delete/", ReviewDeleteView.as_view(), name="review_delete"), # NEW
]

