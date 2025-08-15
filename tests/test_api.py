from django.test import TestCase
from django.urls import reverse
from tests.factories import create_course

class ApiTests(TestCase):
    def test_courses_api_list(self):
        create_course("A")
        create_course("B")
        url = reverse("api:courses-list")  # DRF router name: <basename>-list
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(isinstance(data, list))
        titles = {c["title"] for c in data}
        self.assertIn("A", titles)
        self.assertIn("B", titles)

