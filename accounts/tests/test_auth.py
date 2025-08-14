from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class AuthTests(TestCase):
    def test_login_page_ok(self):
        res = self.client.get(reverse("accounts:login"))
        self.assertEqual(res.status_code, 200)

    def test_register_creates_user(self):
        res = self.client.post(reverse("accounts:register"), {
            "username":"bob",
            "email":"bob@example.com",
            "password1":"Aa!12345678",
            "password2":"Aa!12345678",
        })
        self.assertEqual(res.status_code, 302)
        self.assertTrue(User.objects.filter(username="bob").exists())
