from django.contrib import admin
from django.urls import path, include
from core import views as core_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.home, name='home'),
    path('about/', core_views.about, name='about'),
    path('dashboard/', core_views.dashboard, name='dashboard'),
    path('leaderboard/', core_views.leaderboard, name='leaderboard'),
    path('accounts/', include('accounts.urls')),
    path('courses/', include('courses.urls')),
    path('challenges/', include('challenges.urls')),
    path('portfolio/', include('portfolio.urls')),
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
