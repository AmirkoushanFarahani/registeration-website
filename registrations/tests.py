from django.test import TestCase
from rest_framework.test import APIClient

class RegistrationApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.payload = {
            'first_name': 'ندا', 'last_name': 'آزمون', 'national_id': '1234567891',
            'birth_year': 1390, 'birth_month': 5, 'birth_day': 20, 'gender': 'woman',
            'grade': 'هفتم تا نهم متوسطه اول', 'province': 'تهران', 'city': 'تهران',
            'parent_phone': '', 'email': '', 'address': 'تهران', 'consent': True,
        }

    def test_registration_creates_record_and_returns_tracking_code(self):
        response = self.client.post('/api/v1/registrations/', self.payload, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data['tracking_code'].startswith('IR-'))

    def test_status_requires_matching_national_id(self):
        created = self.client.post('/api/v1/registrations/', self.payload, format='json')
        url = f"/api/v1/registrations/{created.data['tracking_code']}/"
        self.assertEqual(self.client.get(url).status_code, 400)
        self.assertEqual(self.client.get(url, {'national_id': '1234567891'}).status_code, 200)
