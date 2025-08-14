from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from courses.models import Course, Lesson, Enrollment
from challenges.models import Challenge, Submission
from portfolio.models import Project, Review

class Command(BaseCommand):
    help = "Create Staff group with limited CRUD permissions (idempotent)."

    def handle(self, *args, **kwargs):
        staff_group, created = Group.objects.get_or_create(name="Staff")
        models = [Course, Lesson, Enrollment, Challenge, Submission, Project, Review]
        cts = [ContentType.objects.get_for_model(m) for m in models]
        perms = Permission.objects.filter(content_type__in=cts)
        staff_group.permissions.set(perms)
        self.stdout.write(self.style.SUCCESS("Staff group synced with content permissions."))
