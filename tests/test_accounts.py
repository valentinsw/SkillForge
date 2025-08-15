from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.forms import RegistrationForm

User = get_user_model()

class AccountsTests(TestCase):
    def test_registration_form_unique_email(self):
        User.objects.create_user(username="u1", email="taken@example.com", password="x")
        form = RegistrationForm(data={
            "username": "u2",
            "email": "taken@example.com",
            "password1": "Str0ngPass!23",
            "password2": "Str0ngPass!23",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_profile_page_requires_login(self):
        url = reverse("accounts:profile")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)  # redirect to login
        self.assertIn("/accounts/login", resp["Location"])

