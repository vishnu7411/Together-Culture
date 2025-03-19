from django.urls import path
from .views import home, register  # ✅ Ensure both views are imported

urlpatterns = [
    path("home/", home, name="home"),  # Home page
    path("register/", register, name="register"),  # Register page
]
