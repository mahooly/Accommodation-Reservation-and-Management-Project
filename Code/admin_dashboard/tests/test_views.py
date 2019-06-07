from registration.models import CustomUser, Host
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.http import HttpRequest
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from registration.views import EditProfile
from django.core.files.uploadedfile import SimpleUploadedFile
import os
import datetime
import filecmp
import Code.settings as settings
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware

class TestAdminDashboardView(TestCase):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(BASE_DIR, "testMedia/image1.jpg")
    image_path2 = os.path.join(BASE_DIR, "testMedia/image2.jpg")
    request_factory = RequestFactory()

    def setUp(self):
        self.client = Client()
        self.img = SimpleUploadedFile(name='test_image.jpg', content=open(self.image_path, 'rb').read(),
                                  content_type='image/jpeg')
        self.img2 = SimpleUploadedFile(name='test_image2.jpg', content=open(self.image_path2, 'rb').read(),
                                  content_type='image/jpeg')

    def test_adminAccommodationDashboard(self):
        url = reverse('admin_dashboard_accommodations')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_deleteUser(self):
        url = reverse("delete_user", kwargs={"pk": 1})

