from django.urls import path
from .views import register, home

urlpatterns = [
    path("", home, name="home"),  # Home page
    path("register/", register, name="register"),  # Register page
]
