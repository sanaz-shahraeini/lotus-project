from django.contrib import admin
from .models import SMDRRecord

@admin.register(SMDRRecord)
class SMDRRecordAdmin(admin.ModelAdmin):
    list_display = ('date', 'time', 'ext', 'co', 'dial_number', 'call_type', 'duration')
    list_filter = ('date', 'call_type', 'is_incoming', 'is_outgoing', 'is_internal', 'is_system_message')
    search_fields = ('ext', 'co', 'dial_number')
    date_hierarchy = 'date'
