from django.urls import path
from .views import register, home, user_login,manage_events,add_ongoing_event  # ✅ Import user_login
from .views import register, home, user_login  # ✅ Import user_login
from .views import admin_login, admin_dashboard, admin_logout
from .views import registered_members
from .views import pending_members, approve_member, reject_member
from .views import add_event, manage_events
from .views import events_page
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

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
    path('events/', events_page, name='events'),  # Events Page URL
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('login/', views.user_login, name='user_login'),
    path('member-dashboard/', views.member_dashboard, name='member_dashboard'),
    path('logout/', views.member_logout, name='logout'),
    path('submit-review/', views.submit_review, name='submit_review'),
    path('submit-review/success/', views.submit_review_success, name='submit_review_success')



]


