from django import forms
from .models import Project, Review

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ("title","description","repo_url","live_url","is_public")

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("rating","comment")
