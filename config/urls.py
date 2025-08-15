from django.contrib import admin
from django.urls import path, include
from core import views as core_views
from django.conf import settings
from django.conf.urls.static import static

# --- DRF router under the "api" namespace (tests reverse("api:courses-list")) ---
from rest_framework.routers import DefaultRouter
from courses.api import CourseViewSet  # new file you’ll add below

router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="courses")

urlpatterns = [
    path('admin/', admin.site.urls),

    # public pages
    path('', core_views.home, name='home'),
    path('about/', core_views.about, name='about'),
    path('leaderboard/', core_views.leaderboard, name='leaderboard'),

    # private
    path('dashboard/', core_views.dashboard, name='dashboard'),

    # app routes (namespaced)
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('courses/', include(('courses.urls', 'courses'), namespace='courses')),
    path('challenges/', include(('challenges.urls', 'challenges'), namespace='challenges')),
    path('portfolio/', include(('portfolio.urls', 'portfolio'), namespace='portfolio')),

    # API (namespace: "api")
    path('api/', include((router.urls, 'api'), namespace='api')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

