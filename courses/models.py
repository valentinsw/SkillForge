from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.core.exceptions import ValidationError

User = get_user_model()

class Course(models.Model):
    title = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    is_published = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="courses")
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if len(self.short_description) < 10:
            raise ValidationError("Short description is too short.")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self): return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("courses:detail", kwargs={"slug": self.slug})

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=120)
    content = models.TextField()
    order = models.PositiveIntegerField(default=1)
    class Meta: ordering = ["order"]
    def __str__(self): return f"{self.course.title} · {self.title}"

class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    joined_at = models.DateTimeField(auto_now_add=True)
    class Meta: unique_together = ("user","course")
    def __str__(self): return f"{self.user} → {self.course}"
