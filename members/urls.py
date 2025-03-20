from django.urls import path
from .views import register, home, user_login,ongoing_events,add_ongoing_event  # ✅ Import user_login

urlpatterns = [
    path("", home, name="home"),  # Home page
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),  # Login page
    path('ongoing_events/', ongoing_events, name='ongoing_events'),
    path('add_ongoing_event/', add_ongoing_event, name='add_ongoing_event'),

]
