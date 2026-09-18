from django.urls import path
from .views import KanoonAgencyListView, RegistrationListCreateView, RegistrationStatusView

urlpatterns = [
    path('registrations/', RegistrationListCreateView.as_view(), name='registration-create'),
    path('registrations/<str:tracking_code>/', RegistrationStatusView.as_view(), name='registration-status'),
    path('agencies/', KanoonAgencyListView.as_view(), name='agency-list'),
]
