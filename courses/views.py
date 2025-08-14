from django.views.generic import ListView, DetailView
from .models import Course

class CourseListView(ListView):
    template_name = "courses/course_list.html"
    queryset = Course.objects.filter(is_published=True).select_related("created_by")

class CourseDetailView(DetailView):
    template_name = "courses/course_detail.html"
    model = Course
    slug_field = "slug"
    slug_url_kwarg = "slug"
