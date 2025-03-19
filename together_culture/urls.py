from django.contrib import admin
from django.urls import path, include  # Import 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('members.urls')),  # Include the URLs from 'members' app
]
