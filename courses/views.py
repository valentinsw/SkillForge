from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView

from .models import Course, Enrollment


class CourseListView(ListView):
    model = Course
    template_name = "courses/course_list.html"
    context_object_name = "courses"
    paginate_by = 12

    def get_queryset(self):
        qs = Course.objects.filter(is_published=True).order_by("-created_at")
        q = (self.request.GET.get("q") or "").strip()
        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(short_description__icontains=q) |
                Q(description__icontains=q)
            ).distinct()
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = (self.request.GET.get("q") or "").strip()
        return ctx


class CourseDetailView(DetailView):
    model = Course
    template_name = "courses/course_detail.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        # Only published courses are viewable to regular users
        return Course.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            ctx["is_enrolled"] = Enrollment.objects.filter(
                user=user, course=self.object
            ).exists()
        else:
            ctx["is_enrolled"] = False
        return ctx


class CourseEnrollView(LoginRequiredMixin, View):
    """POST to enroll current user into the course."""
    def post(self, request, slug):
        course = get_object_or_404(Course, slug=slug, is_published=True)
        _, created = Enrollment.objects.get_or_create(user=request.user, course=course)
        if created:
            messages.success(request, f"You enrolled in “{course.title}”.")
        else:
            messages.info(request, f"You're already enrolled in “{course.title}”.")
        return redirect(reverse("courses:detail", kwargs={"slug": course.slug}))


class CourseUnenrollView(LoginRequiredMixin, View):
    """POST to leave the course."""
    def post(self, request, slug):
        course = get_object_or_404(Course, slug=slug, is_published=True)
        deleted, _ = Enrollment.objects.filter(user=request.user, course=course).delete()
        if deleted:
            messages.success(request, f"You left “{course.title}”.")
        else:
            messages.info(request, f"You were not enrolled in “{course.title}”.")
        return redirect(reverse("courses:detail", kwargs={"slug": course.slug}))

