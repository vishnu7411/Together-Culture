from django.urls import path
from .views import register, home, user_login  # ✅ Import user_login

urlpatterns = [
    path("", home, name="home"),  # Home page
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),  # Login page
]
