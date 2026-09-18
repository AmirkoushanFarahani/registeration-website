from django.contrib import admin
from .models import StudentRegistration

@admin.register(StudentRegistration)
class StudentRegistrationAdmin(admin.ModelAdmin):
    list_display = ('tracking_code', 'first_name', 'last_name', 'national_id', 'province', 'city', 'created_at')
    search_fields = ('tracking_code', 'national_id', 'first_name', 'last_name', 'parent_phone')
    list_filter = ('province', 'gender', 'grade', 'created_at')
    readonly_fields = ('tracking_code', 'consent_at', 'created_at', 'updated_at')
