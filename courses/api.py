from rest_framework import serializers, viewsets
from .models import Course

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "title", "slug", "short_description", "is_published", "created_at"]

class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.filter(is_published=True).order_by("id")
    serializer_class = CourseSerializer

