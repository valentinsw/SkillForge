from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from portfolio.models import Project

class ProjectCRUDTests(TestCase):
    def setUp(self):
        self.u = User.objects.create_user("kate", password="pass12345")
        self.client.login(username="kate", password="pass12345")

    def test_create_project(self):
        res = self.client.post(reverse("portfolio:create"), {
            "title":"My App","description":"Desc","repo_url":"","live_url":"","is_public":True
        })
        self.assertEqual(res.status_code, 302)
        self.assertTrue(Project.objects.filter(owner=self.u, title="My App").exists())
