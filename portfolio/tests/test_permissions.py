from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from portfolio.models import Project

class ProjectPermissionsTests(TestCase):
    def setUp(self):
        self.a = User.objects.create_user("a", password="pass12345")
        self.b = User.objects.create_user("b", password="pass12345")
        self.client.login(username="a", password="pass12345")

    def test_owner_only_edit(self):
        p = Project.objects.create(owner=self.a, title="X", description="D")
        url = reverse("portfolio:edit", args=[p.pk])
        self.assertEqual(self.client.get(url).status_code, 200)
        self.client.logout()
        self.client.login(username="b", password="pass12345")
        self.assertEqual(self.client.get(url).status_code, 403)  # UserPassesTestMixin returns 403 by default
