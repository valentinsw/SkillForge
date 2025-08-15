from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from .models import Profile

User = get_user_model()


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in use.")
        return email


class ProfileForm(forms.ModelForm):
    # Extra fields that actually belong to auth.User
    first_name = forms.CharField(
        max_length=150, required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "First name"})
    )
    last_name = forms.CharField(
        max_length=150, required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Last name"})
    )

    class Meta:
        model = Profile
        fields = ("display_name", "bio")  # Model fields only
        widgets = {
            "display_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Public display name"}),
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Short bio"}),
        }

    def __init__(self, *args, user=None, **kwargs):
        """
        Expect the logged-in user so we can prefill and save first/last name.
        """
        super().__init__(*args, **kwargs)
        self._user = user
        if user is not None:
            self.fields["first_name"].initial = user.first_name
            self.fields["last_name"].initial = user.last_name

    def save(self, commit=True):
        """
        Save Profile normally, and also persist first/last name on the auth.User.
        """
        profile = super().save(commit=False)

        if self._user is not None and self.is_valid():
            self._user.first_name = self.cleaned_data.get("first_name", "") or ""
            self._user.last_name = self.cleaned_data.get("last_name", "") or ""
            if commit:
                self._user.save()

        if commit:
            profile.save()
        return profile

