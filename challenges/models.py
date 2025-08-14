from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from courses.models import Course

User = get_user_model()

class Challenge(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="challenges")
    title = models.CharField(max_length=120)
    prompt = models.TextField()
    deadline = models.DateTimeField(null=True, blank=True)
    def clean(self):
        if self.deadline and self.deadline < timezone.now():
            raise ValidationError("Deadline must be in the future.")
    def __str__(self): return self.title

class Submission(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name="submissions")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submissions")
    text_answer = models.TextField(blank=True)
    attachment = models.FileField(upload_to="submissions/", blank=True)
    score = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ["-created_at"]
    def __str__(self): return f"{self.author} → {self.challenge}"
