from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class PagesTests(TestCase):
    def test_home_ok(self):
        res = self.client.get(reverse("home"))
        self.assertEqual(res.status_code, 200)

    def test_about_ok(self):
        res = self.client.get(reverse("about"))
        self.assertEqual(res.status_code, 200)

    def test_dashboard_login_required(self):
        res = self.client.get(reverse("dashboard"))
        self.assertEqual(res.status_code, 302)
        self.assertIn("/accounts/login/", res.headers["Location"])
        u = User.objects.create_user("alice", password="pass12345")
        self.client.login(username="alice", password="pass12345")
        res2 = self.client.get(reverse("dashboard"))
        self.assertEqual(res2.status_code, 200)
