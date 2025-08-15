from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError
from tests.factories import create_user, create_project, review
from portfolio.models import Review

class PortfolioTests(TestCase):
    def test_review_rating_validation(self):
        owner = create_user("owner")
        project = create_project(owner=owner)
        reviewer = create_user("rev")
        bad = Review(project=project, reviewer=reviewer, rating=6, comment="too high")
        with self.assertRaises(ValidationError):
            bad.full_clean()  # triggers model validators

    def test_review_edit_permissions(self):
        owner = create_user("owner", password="x")
        other = create_user("other", password="x")
        rev_user = create_user("rev", password="x")
        p = create_project(owner=owner)
        r = review(project=p, reviewer=rev_user, rating=5)

        # Reviewer can open edit
        self.client.login(username="rev", password="x")
        url = reverse("portfolio:review_edit", args=[r.pk])
        self.assertEqual(self.client.get(url).status_code, 200)

        # Different user gets 403
        self.client.logout()
        self.client.login(username="other", password="x")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 403)

        # Project owner can edit
        self.client.logout()
        self.client.login(username="owner", password="x")
        self.assertEqual(self.client.get(url).status_code, 200)

