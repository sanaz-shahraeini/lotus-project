from django.contrib import admin
from .models import Records, SMDRRecord, Users, Groups, Infos, Permissions, ContactInfo, Log, lices, SupportMessage

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'lastname', 'email', 'extension', 'active', 'online', 'groupname')
    list_filter = ('active', 'online', 'group', 'needs_password_change')
    search_fields = ('username', 'name', 'lastname', 'email', 'extension')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Groups)
class GroupsAdmin(admin.ModelAdmin):
    list_display = ('pename', 'enname', 'active')
    list_filter = ('active',)
    search_fields = ('pename', 'enname')

@admin.register(Infos)
class InfosAdmin(admin.ModelAdmin):
    list_display = ('user', 'phonenumber', 'province', 'city', 'gender')
    list_filter = ('province', 'gender', 'military', 'maritalstatus', 'educationdegree')
    search_fields = ('user__username', 'user__name', 'phonenumber', 'nationalcode')

@admin.register(Permissions)
class PermissionsAdmin(admin.ModelAdmin):
    list_display = ('user', 'can_view', 'can_write', 'can_delete', 'can_modify', 'errorsreport')
    list_filter = ('can_view', 'can_write', 'can_delete', 'can_modify', 'errorsreport')
    search_fields = ('user__username', 'user__name')

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'province', 'phone_number')
    list_filter = ('province',)
    search_fields = ('user__username', 'user__name', 'phone_number')

@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ('user', 'errCode', 'errMessage', 'ip', 'created_at')
    list_filter = ('errCode', 'byWho', 'created_at')
    search_fields = ('user__username', 'errCode', 'errMessage', 'ip')
    readonly_fields = ('created_at',)

@admin.register(lices)
class licesAdmin(admin.ModelAdmin):
    list_display = ('lice', 'active', 'version', 'created_at')
    list_filter = ('active', 'version')
    search_fields = ('lice',)
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Records)
class RecordsAdmin(admin.ModelAdmin):
    list_display = ('date', 'hour', 'extension', 'urbanline', 'contactnumber', 'calltype', 'durationtime')
    list_filter = ('date', 'calltype', 'extension', 'urbanline')
    search_fields = ('extension', 'contactnumber', 'urbanline')

@admin.register(SMDRRecord)
class SMDRRecordAdmin(admin.ModelAdmin):
    list_display = ('date', 'time', 'ext', 'co', 'dial_number', 'call_type', 'duration')
    list_filter = ('date', 'call_type', 'is_incoming', 'is_outgoing', 'is_internal', 'is_system_message')
    search_fields = ('ext', 'co', 'dial_number')
    date_hierarchy = 'date'

@admin.register(SupportMessage)
class SupportMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'message_preview', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'message')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    
    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'پیام'
