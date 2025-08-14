from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from courses.models import Course

class CourseViewsTests(TestCase):
    def setUp(self):
        self.u = User.objects.create_user("inst", password="pass12345")

    def test_course_list_empty(self):
        res = self.client.get(reverse("courses:list"))
        self.assertEqual(res.status_code, 200)

    def test_course_detail_slug(self):
        c = Course.objects.create(title="Django 101", short_description="Basics course",
                                  description="...", created_by=self.u, is_published=True)
        res = self.client.get(c.get_absolute_url())
        self.assertEqual(res.status_code, 200)
