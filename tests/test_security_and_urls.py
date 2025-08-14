from django.test import TestCase
from django.urls import reverse, resolve

class UrlsTests(TestCase):
    def test_home_url(self):
        resolver = resolve("/")
        self.assertEqual(resolver.view_name, "home")

    def test_courses_url(self):
        self.assertEqual(resolve("/courses/").view_name, "courses:list")
