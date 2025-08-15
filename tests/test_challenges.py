from django.test import TestCase
from django.urls import reverse
from tests.factories import create_user, create_challenge, submit

class ChallengesTests(TestCase):
    def setUp(self):
        self.student = create_user("student", password="p")
        self.other = create_user("other", password="p")
        self.ch = create_challenge(title="Blog Engine")

    def test_list_and_detail_pages(self):
        list_url = reverse("challenges:list")
        self.assertEqual(self.client.get(list_url).status_code, 200)

        detail_url = reverse("challenges:detail", args=[self.ch.pk])
        resp = self.client.get(detail_url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Blog Engine")

    def test_submission_create_requires_login(self):
        url = reverse("challenges:submission_create", args=[self.ch.pk])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/accounts/login", resp["Location"])

    def test_submission_edit_only_author(self):
        s = submit(author=self.student, challenge=self.ch)
        edit_url = reverse("challenges:submission_edit", args=[s.pk])

        # Author can access
        self.client.login(username="student", password="p")
        self.assertEqual(self.client.get(edit_url).status_code, 200)

        # Other user forbidden
        self.client.logout()
        self.client.login(username="other", password="p")
        self.assertEqual(self.client.get(edit_url).status_code, 403)

