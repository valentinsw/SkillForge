from django import forms
from .models import Project, Review


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["title", "description", "repo_url", "live_url", "is_public"]


class ReviewForm(forms.ModelForm):
    # UI + server validation
    rating = forms.IntegerField(
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(attrs={"min": 1, "max": 5, "step": 1}),
        help_text="Rate 1–5",
        label="Rating",
    )

    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "comment": forms.Textarea(attrs={"rows": 4}),
        }

