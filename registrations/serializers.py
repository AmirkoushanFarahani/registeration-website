import re
from rest_framework import serializers
from .models import KanoonAgency, StudentRegistration

def normalize_digits(value):
    return str(value).translate(str.maketrans('۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩', '01234567890123456789'))

def valid_national_id(value):
    value = normalize_digits(value)
    if not re.fullmatch(r'\d{10}', value) or value == value[0] * 10:
        return False
    total = sum(int(digit) * (10 - index) for index, digit in enumerate(value[:9]))
    check = total % 11 if total % 11 < 2 else 11 - (total % 11)
    return check == int(value[-1])

class StudentRegistrationSerializer(serializers.ModelSerializer):
    birth_year = serializers.IntegerField(write_only=True, min_value=1300, max_value=1500)
    birth_month = serializers.IntegerField(write_only=True, min_value=1, max_value=12)
    birth_day = serializers.IntegerField(write_only=True, min_value=1, max_value=31)
    consent = serializers.BooleanField(write_only=True)
    agency_id = serializers.PrimaryKeyRelatedField(source='agency', queryset=KanoonAgency.objects.all(), required=False, allow_null=True, write_only=True)

    class Meta:
        model = StudentRegistration
        fields = ('tracking_code', 'first_name', 'last_name', 'national_id', 'birth_year', 'birth_month', 'birth_day',
                  'gender', 'grade', 'province', 'city', 'agency_id', 'parent_phone', 'email', 'address', 'consent')
        read_only_fields = ('tracking_code',)
        extra_kwargs = {
            'first_name': {'trim_whitespace': True}, 'last_name': {'trim_whitespace': True},
            'parent_phone': {'required': False, 'allow_blank': True}, 'email': {'required': False, 'allow_blank': True},
        }

    def validate_national_id(self, value):
        value = normalize_digits(value).replace(' ', '')
        if not valid_national_id(value):
            raise serializers.ValidationError('کد ملی واردشده معتبر نیست.')
        return value

    def validate_parent_phone(self, value):
        value = normalize_digits(value).replace(' ', '').replace('-', '')
        if value and not re.fullmatch(r'09\d{9}', value):
            raise serializers.ValidationError('شماره همراه باید با ۰۹ شروع شود و ۱۱ رقم باشد.')
        return value

    def validate_consent(self, value):
        if not value:
            raise serializers.ValidationError('تأیید شرایط و حریم خصوصی الزامی است.')
        return value

    def validate(self, attrs):
        if attrs['birth_month'] > 6 and attrs['birth_day'] > 30:
            raise serializers.ValidationError({'birth_day': 'این ماه حداکثر ۳۰ روز دارد.'})
        agency = attrs.get('agency')
        if agency and agency.province != attrs['province']:
            raise serializers.ValidationError({'agency_id': 'آموزشگاه انتخاب‌شده متعلق به استان انتخابی نیست.'})
        return attrs

    def create(self, validated_data):
        year, month, day = (validated_data.pop('birth_year'), validated_data.pop('birth_month'), validated_data.pop('birth_day'))
        validated_data.pop('consent')
        validated_data['birth_date_jalali'] = f'{year:04d}/{month:02d}/{day:02d}'
        return super().create(validated_data)

class RegistrationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentRegistration
        fields = ('tracking_code', 'first_name', 'last_name', 'grade', 'province', 'city', 'created_at')

class KanoonAgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = KanoonAgency
        fields = ('id', 'province', 'city', 'office_name', 'address', 'phone_numbers')
