from django.contrib import admin
from .models import Member

# Register the Member model
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'membership_type', 'gender')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('membership_type', 'gender')

# Customizing Django Admin Branding
admin.site.site_header = "Together Culture Admin"
admin.site.site_title = "Together Culture Admin Panel"
admin.site.index_title = "Welcome to Together Culture Admin"

# events/admin.py
from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_type', 'location', 'capacity', 'event_date', 'event_time')
