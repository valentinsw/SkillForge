from django.db.models import Q
from django.views.generic import ListView, DetailView
from .models import Course


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
                Q(title__icontains=q)
                | Q(short_description__icontains=q)
                | Q(description__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        q = (self.request.GET.get("q") or "").strip()
        ctx["q"] = q
        ctx["result_count"] = self.get_queryset().count()
        return ctx


class CourseDetailView(DetailView):
    model = Course
    slug_field = "slug"
    slug_url_kwarg = "slug"
    template_name = "courses/course_detail.html"
    context_object_name = "course"

