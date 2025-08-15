from django.test import TestCase
from django.urls import reverse
from tests.factories import create_user, create_course, add_lesson, enroll
from courses.models import Enrollment

class CoursesTests(TestCase):
    def setUp(self):
        self.author = create_user("author")
        self.user = create_user("student", password="pass1234")
        self.c1 = create_course("REST APIs with DRF", created_by=self.author, is_published=True, slug="drf")
        self.c2 = create_course("Django CBVs Deep Dive", created_by=self.author, is_published=True, slug="cbvs")
        self.c3 = create_course("Draft Course", created_by=self.author, is_published=False, slug="draft")
        add_lesson(self.c1, "Intro", 1)

    def test_course_list_shows_only_published(self):
        url = reverse("courses:list")
        resp = self.client.get(url)
        self.assertContains(resp, "REST APIs with DRF")
        self.assertContains(resp, "Django CBVs Deep Dive")
        self.assertNotContains(resp, "Draft Course")

    def test_course_list_search_q_filters(self):
        url = reverse("courses:list")
        resp = self.client.get(url, {"q": "DRF"})
        self.assertContains(resp, "REST APIs with DRF")
        self.assertNotContains(resp, "Django CBVs Deep Dive")

    def test_course_detail_renders_lessons(self):
        url = reverse("courses:detail", args=[self.c1.slug])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Lessons")
        self.assertContains(resp, "Intro")

    def test_enroll_unenroll_flow(self):
        self.client.login(username="student", password="pass1234")

        # Enroll
        enroll_url = reverse("courses:enroll", args=[self.c1.slug])
        resp = self.client.post(enroll_url, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(Enrollment.objects.filter(user=self.user, course=self.c1).exists())
        self.assertContains(resp, "Leave course")  # button changes when enrolled

        # Unenroll
        unenroll_url = reverse("courses:unenroll", args=[self.c1.slug])
        resp = self.client.post(unenroll_url, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(Enrollment.objects.filter(user=self.user, course=self.c1).exists())
        self.assertContains(resp, "Enroll")

