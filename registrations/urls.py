from django.urls import path
from .views import RegistrationListCreateView, RegistrationStatusView

urlpatterns = [
    path('registrations/', RegistrationListCreateView.as_view(), name='registration-create'),
    path('registrations/<str:tracking_code>/', RegistrationStatusView.as_view(), name='registration-status'),
]
