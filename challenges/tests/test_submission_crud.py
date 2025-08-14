from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from courses.models import Course
from challenges.models import Challenge, Submission
from django.utils import timezone
from datetime import timedelta

class SubmissionCRUDTests(TestCase):
    def setUp(self):
        self.u = User.objects.create_user("alice", password="pass12345")
        self.client.login(username="alice", password="pass12345")
        self.course = Course.objects.create(title="Django 101", short_description="Basics course",
                                            description="...", created_by=self.u, is_published=True)
        self.challenge = Challenge.objects.create(course=self.course, title="Warmup", prompt="Say hi",
                                                  deadline=timezone.now()+timedelta(days=1))

    def test_create_submission(self):
        url = reverse("challenges:submit", args=[self.challenge.pk])
        res = self.client.post(url, {"text_answer":"Hello"})
        self.assertEqual(res.status_code, 302)
        self.assertTrue(Submission.objects.filter(author=self.u, challenge=self.challenge).exists())
