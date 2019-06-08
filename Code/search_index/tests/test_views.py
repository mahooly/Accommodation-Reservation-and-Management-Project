from django.test import TestCase, Client, RequestFactory
from django.urls import reverse


class TestUserRegistrationView(TestCase):
    request_factory = RequestFactory()

    def setUp(self):
        self.client = Client()

    def test_searchView(self):
        url = reverse('search')

        # test with empty data
        response = self.client.get(url, {})
        self.assertEqual(response.status_code, 200)

        # test with valid data
        req_data = {"expression": "Sharif University"}
        response = self.client.get(url, req_data)
        self.assertEqual(response.status_code, 200)

        req_data = {"province": "Tehran", "hotel": False, "motel": True, "house": True, "city": "Tehran"}
        response = self.client.get(url, req_data)
        self.assertEqual(response.status_code, 200)
