from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet

router = DefaultRouter()
router.register("courses", CourseViewSet, basename="api-courses")
urlpatterns = [ path("", include(router.urls)) ]
