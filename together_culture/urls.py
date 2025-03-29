from django.contrib import admin
from django.urls import path, include  # Import 'include'
from events import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('members.urls')),  # Include the URLs from 'members' app
    path('review/', views.review_page, name='review')
]
