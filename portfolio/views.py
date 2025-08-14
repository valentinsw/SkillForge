from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Project, Review
from .forms import ProjectForm, ReviewForm

class MyProjectsListView(LoginRequiredMixin, ListView):
    template_name = "portfolio/project_list.html"
    def get_queryset(self):
        return self.request.user.projects.all()

class ProjectDetailView(LoginRequiredMixin, DetailView):
    template_name = "portfolio/project_detail.html"
    model = Project

class OwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().owner == self.request.user

class ProjectCreateView(LoginRequiredMixin, CreateView):
    template_name = "forms/form.html"
    model = Project
    form_class = ProjectForm
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy("portfolio:projects")

class ProjectUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    template_name = "forms/form.html"
    model = Project
    form_class = ProjectForm
    def get_success_url(self):
        return reverse_lazy("portfolio:projects")

class ProjectDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    template_name = "forms/confirm_delete.html"
    model = Project
    def get_success_url(self):
        return reverse_lazy("portfolio:projects")

class ReviewCreateView(LoginRequiredMixin, CreateView):
    template_name = "forms/form.html"
    model = Review
    form_class = ReviewForm
    def form_valid(self, form):
        project = Project.objects.get(pk=self.kwargs["project_pk"])
        form.instance.project = project
        form.instance.reviewer = self.request.user
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy("portfolio:detail", kwargs={"pk": self.kwargs["project_pk"]})
