import uuid
from django.db import models

class StudentRegistration(models.Model):
    class Gender(models.TextChoices):
        WOMAN = 'woman', 'زن'
        MAN = 'man', 'مرد'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tracking_code = models.CharField(max_length=20, unique=True, editable=False)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=100)
    national_id = models.CharField(max_length=10, unique=True)
    birth_date_jalali = models.CharField(max_length=10)
    gender = models.CharField(max_length=10, choices=Gender.choices)
    grade = models.CharField(max_length=100)
    province = models.CharField(max_length=80)
    city = models.CharField(max_length=80)
    parent_phone = models.CharField(max_length=11, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField()
    consent_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'ثبت‌نام دانش‌آموز'
        verbose_name_plural = 'ثبت‌نام‌های دانش‌آموزان'

    def save(self, *args, **kwargs):
        if not self.tracking_code:
            self.tracking_code = f'IR-{uuid.uuid4().hex[:8].upper()}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.tracking_code})'
