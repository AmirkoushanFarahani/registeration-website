from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import StudentRegistration
from .serializers import RegistrationStatusSerializer, StudentRegistrationSerializer, normalize_digits

class RegistrationListCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = StudentRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        registration = serializer.save()
        return Response({'tracking_code': registration.tracking_code, 'message': 'درخواست شما با موفقیت ثبت شد.'}, status=status.HTTP_201_CREATED)

class RegistrationStatusView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, tracking_code):
        national_id = normalize_digits(request.query_params.get('national_id', '')).replace(' ', '')
        if not national_id:
            return Response({'detail': 'کد ملی برای پیگیری الزامی است.'}, status=status.HTTP_400_BAD_REQUEST)
        registration = get_object_or_404(StudentRegistration, tracking_code=tracking_code, national_id=national_id)
        return Response(RegistrationStatusSerializer(registration).data)
