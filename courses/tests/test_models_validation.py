from django.test import TestCase
from django.contrib.auth.models import User
from courses.models import Course
from django.core.exceptions import ValidationError

class CourseValidationTests(TestCase):
    def test_short_description_validation(self):
        u = User.objects.create_user("inst", password="pass12345")
        c = Course(title="X", short_description="short", description="...", created_by=u)
        with self.assertRaises(ValidationError):
            c.clean()
