from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from .models import Challenge, Submission
from .forms import SubmissionForm

class ChallengeListView(LoginRequiredMixin, ListView):
    template_name = "challenges/challenge_list.html"
    model = Challenge

class ChallengeDetailView(LoginRequiredMixin, DetailView):
    template_name = "challenges/challenge_detail.html"
    model = Challenge

class UserIsOwnerMixin(UserPassesTestMixin):
    def test_func(self): return self.get_object().author == self.request.user

class SubmissionCreateView(LoginRequiredMixin, CreateView):
    template_name = "forms/form.html"
    form_class = SubmissionForm

    def dispatch(self, request, *args, **kwargs):
        self.challenge = get_object_or_404(Challenge, pk=kwargs["challenge_pk"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.challenge = self.challenge
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("challenges:detail", kwargs={"pk": self.challenge.pk})

class SubmissionUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    template_name = "forms/form.html"
    model = Submission
    form_class = SubmissionForm
    def get_success_url(self):
        return reverse_lazy("challenges:detail", kwargs={"pk": self.object.challenge.pk})

class SubmissionDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    template_name = "forms/confirm_delete.html"
    model = Submission
    def get_success_url(self):
        return reverse_lazy("challenges:detail", kwargs={"pk": self.object.challenge.pk})
