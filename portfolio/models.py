from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Q

User = get_user_model()


class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    title = models.CharField(max_length=140)
    description = models.TextField()
    repo_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class Review(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="reviews")
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="1 (worst) to 5 (best)",
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # DB safety: enforce 1..5 and one review per user per project
        constraints = [
            models.CheckConstraint(
                check=Q(rating__gte=1) & Q(rating__lte=5),
                name="portfolio_review_rating_between_1_and_5",
            ),
            models.UniqueConstraint(
                fields=["project", "reviewer"],
                name="portfolio_one_review_per_user_per_project",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.reviewer} on {self.project}"

