from django.contrib import admin
from .models import KanoonAgency, StudentRegistration

@admin.register(KanoonAgency)
class KanoonAgencyAdmin(admin.ModelAdmin):
    list_display = ('office_name', 'province', 'city', 'phone_numbers')
    search_fields = ('office_name', 'province', 'city', 'address', 'phone_numbers')
    list_filter = ('province',)

@admin.register(StudentRegistration)
class StudentRegistrationAdmin(admin.ModelAdmin):
    list_display = ('tracking_code', 'first_name', 'last_name', 'national_id', 'province', 'city', 'agency', 'created_at')
    search_fields = ('tracking_code', 'national_id', 'first_name', 'last_name', 'parent_phone')
    list_filter = ('province', 'gender', 'grade', 'created_at')
    readonly_fields = ('tracking_code', 'consent_at', 'created_at', 'updated_at')
