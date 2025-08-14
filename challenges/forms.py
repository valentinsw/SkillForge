from django import forms
from .models import Submission

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ("text_answer","attachment")

    def clean_attachment(self):
        f = self.cleaned_data.get("attachment")
        if not f:
            return f
        if f.size > 5*1024*1024:
            raise forms.ValidationError("File too large (5MB max).")
        if not f.name.lower().endswith((".pdf",".zip",".txt",".md",".py")):
            raise forms.ValidationError("Unsupported file type.")
        return f
