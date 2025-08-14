from django.urls import path
from .views import (ChallengeListView, ChallengeDetailView,
                    SubmissionCreateView, SubmissionUpdateView, SubmissionDeleteView)

app_name = "challenges"
urlpatterns = [
    path("", ChallengeListView.as_view(), name="list"),
    path("<int:pk>/", ChallengeDetailView.as_view(), name="detail"),
    path("<int:challenge_pk>/submit/", SubmissionCreateView.as_view(), name="submit"),
    path("submission/<int:pk>/edit/", SubmissionUpdateView.as_view(), name="submission_edit"),
    path("submission/<int:pk>/delete/", SubmissionDeleteView.as_view(), name="submission_delete"),
]
