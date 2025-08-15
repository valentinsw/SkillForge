from django.db.models import Avg, Count
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

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        p = self.object
        agg = p.reviews.aggregate(avg=Avg("rating"), n=Count("id"))
        ctx["avg_rating"] = agg["avg"]
        ctx["reviews_count"] = agg["n"]

        user = self.request.user
        user_has_reviewed = (
            p.reviews.filter(reviewer=user).exists() if user.is_authenticated else False
        )
        ctx["user_has_reviewed"] = user_has_reviewed
        ctx["can_review"] = user.is_authenticated and user != p.owner and not user_has_reviewed
        return ctx


class OwnerRequiredMixin(UserPassesTestMixin):
    # Return 403 for authenticated users who fail the check
    raise_exception = True

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


# --- Permissions for review edit/delete (return 403 when denied) -----------------

class ReviewEditPermissionMixin(UserPassesTestMixin):
    """Edit allowed for review author, project owner, or site staff."""
    raise_exception = True

    def test_func(self):
        review = self.get_object()
        u = self.request.user
        return u.is_authenticated and (
            u.is_staff or review.reviewer_id == u.id or review.project.owner_id == u.id
        )


class ReviewDeletePermissionMixin(UserPassesTestMixin):
    """Delete allowed for review author, site staff, or project owner."""
    raise_exception = True

    def test_func(self):
        review = self.get_object()
        u = self.request.user
        return u.is_authenticated and (
            u.is_staff or review.reviewer_id == u.id or review.project.owner_id == u.id
        )


class ReviewUpdateView(LoginRequiredMixin, ReviewEditPermissionMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = "forms/form.html"

    def get_success_url(self):
        return reverse_lazy("portfolio:detail", kwargs={"pk": self.object.project_id})


class ReviewDeleteView(LoginRequiredMixin, ReviewDeletePermissionMixin, DeleteView):
    model = Review
    template_name = "forms/confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("portfolio:detail", kwargs={"pk": self.object.project_id})

