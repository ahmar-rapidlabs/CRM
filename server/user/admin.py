from django.contrib import admin
from .models import User, Profile, Event

admin.site.register(User)
admin.site.register(Profile)
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date', 'created_by']
    list_filter = ['start_date', 'end_date', 'created_by']
    search_fields = ['name', 'description']
