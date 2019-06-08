from registration.models import CustomUser, Host
from accommodation.models import Amenity, Accommodation
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.http import HttpRequest
from ..views import AdminAccommodationDashboard
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

    def createUser(self):
        the_user = CustomUser.objects.create(username="armin_gm", email="arminbehnamnia@gmail.com",
                                  last_name="armin", first_name="behnamnia",
                                  birth_date=datetime.date(year=1995, month=11, day=7), is_host=False, gender="male",
                                  image=self.img)
        the_user.save()
        return the_user

    def createHost(self):
        the_user = self.createUser()
        the_host = Host.objects.create(user=the_user, passport_pic=self.img,
                    home_address="Azadi St., Sharif University of Tech", phone_number="02144445555",
                    city="Tehran")
        the_host.save()
        return the_host

    def createAmenity(self):
        exp_data = {"name":"Couch", "label":"Red"}
        amenity = Amenity.objects.create(name="Couch", label="Red")
        amenity.save()
        return amenity

    def setUp(self):
        self.client = Client()
        self.img = SimpleUploadedFile(name='test_image.jpg', content=open(self.image_path, 'rb').read(),
                                  content_type='image/jpeg')
        self.img2 = SimpleUploadedFile(name='test_image2.jpg', content=open(self.image_path2, 'rb').read(),
                                  content_type='image/jpeg')

    def test_adminAccommodationDashboard(self):
        the_host = self.createHost()
        the_amenity = self.createAmenity()
        the_host.user.is_superuser = True
        the_user = the_host.user
        url = reverse('admin_dashboard_accommodations')
        self.client.force_login(the_user)
        aa_dashboard = AdminAccommodationDashboard.as_view()
        req_data = {"owner":the_host, "title":"Model_Ghoo", "description":"A decent luxury hotel.",
                    "accommodation_type": "هتل", "province":"Tehran", "city":"Tehran", "address": "1234",
                    "phone": "02144239859", "email": "armin@gmail.com", "amenity": the_amenity}
        req = self.request_factory.get(url, req_data)
        aa_dashboard(req)
        # aa_dashboard.get_queryset()
        # aa_dashboard.get_context_data()
#        response = self.client.get(url)
#        self.assertEqual(response.status_code, 200)

    # def test_deleteUser(self):
    #     the_user = self.createUser()
    #     url = reverse("delete_user", kwargs={"pk": the_user.pk})
    #     self.assertEqual(CustomUser.objects.count(), 1)
    #     self.client.get(url)
    #     self.assertEqual(CustomUser.objects.count(), 0)
    #
