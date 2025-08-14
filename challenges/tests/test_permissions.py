from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from courses.models import Course
from challenges.models import Challenge, Submission
from django.utils import timezone
from datetime import timedelta

class SubmissionPermissionTests(TestCase):
    def setUp(self):
        self.u1 = User.objects.create_user("u1", password="pass12345")
        self.u2 = User.objects.create_user("u2", password="pass12345")
        self.course = Course.objects.create(title="C", short_description="short description ok",
                                            description="...", created_by=self.u1, is_published=True)
        self.challenge = Challenge.objects.create(course=self.course, title="Ch", prompt="P",
                                                  deadline=timezone.now()+timedelta(days=1))
        self.sub = Submission.objects.create(challenge=self.challenge, author=self.u1, text_answer="A")

    def test_non_owner_cannot_edit(self):
        self.client.login(username="u2", password="pass12345")
        res = self.client.get(reverse("challenges:submission_edit", args=[self.sub.pk]))
        self.assertEqual(res.status_code, 403)
