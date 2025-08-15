from django.test import TestCase
from django.urls import reverse
from tests.factories import create_user, create_course, create_project, submit

class CoreTests(TestCase):
    def test_home_context_and_status(self):
        create_course(title="Published A")
        create_course(title="Published B")
        create_project()  # to bump public projects count
        url = reverse("home")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("featured_courses", resp.context)
        self.assertIn("community_projects", resp.context)
        self.assertIn("stats", resp.context)

    def test_dashboard_requires_login(self):
        url = reverse("dashboard")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/accounts/login", resp["Location"])

    def test_leaderboard_async(self):
        url = reverse("leaderboard")
        # Even with no data, should render 200
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

