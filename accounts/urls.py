from django.urls import path
from django.contrib.auth import views as auth_views
from .views import RegisterView, ProfileUpdateView

app_name = "accounts"

urlpatterns = [
    # Auth
    path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    # Registration
    path("register/", RegisterView.as_view(), name="register"),

    # Profile (user-editable first/last name + profile fields)
    path("profile/", ProfileUpdateView.as_view(), name="profile"),
]

