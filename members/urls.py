from django.urls import path
from .views import register, home, user_login,manage_events,add_ongoing_event  # ✅ Import user_login
from .views import register, home, user_login  # ✅ Import user_login
from .views import admin_login, admin_dashboard, admin_logout
from .views import registered_members
from .views import pending_members, approve_member, reject_member
from .views import add_event, manage_events

urlpatterns = [
    path("", home, name="home"),  # Home page
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),  # Login page
    path('manage-events/', manage_events, name='manage_events'),
    path('add_ongoing_event/', add_ongoing_event, name='add_ongoing_event'),
    path("admin-login/", admin_login, name="admin_login"),
    path("admin-dashboard/", admin_dashboard, name="admin_dashboard"),
    path("admin-logout/", admin_logout, name="admin_logout"),
    path("registered-members/", registered_members, name="registered_members"),
    path("pending-members/", pending_members, name="pending_members"),
    path("approve-member/<int:member_id>/", approve_member, name="approve_member"),
    path("reject-member/<int:member_id>/", reject_member, name="reject_member"),
    path('add-event/', add_event, name='add_event'),
    path('manage-events/', manage_events, name='manage_events'),

]
