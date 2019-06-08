from registration.models import CustomUser, Host
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.http import HttpRequest
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from registration.views import EditProfile, HostRegistration
from django.core.files.uploadedfile import SimpleUploadedFile
import os
import datetime
import filecmp
import Code.settings as settings
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.middleware import MessageMiddleware

class TestUserRegistrationView(TestCase):
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

    def createUser(self):
        the_user = CustomUser.objects.create(username="armin_gm", email="arminbehnamnia@gmail.com",
                                  last_name="armin", first_name="behnamnia",
                                  birth_date=datetime.date(year=1995, month=11, day=7), is_host=False, gender="male",
                                  image=self.img)
        the_user.save()
        return the_user

    def test_registration(self):
        url = reverse('register')

        # test req method GET
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # test req method POST with empty data
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CustomUser.objects.count(), 0)

        # test req method POST with valid data
        req_data = {
            "username" : "armin_gm", "password1" : "armin123456", "password2" : "armin123456", "first_name" : "armin"
            , "last_name" : "behnamnia", "email" : "arminbehnamnia@gmail.com", "gender" : "male"
            , "birth_date" : datetime.date(year=1995, month=11, day=7), "image" : self.img
        }
        response = self.client.post(url, req_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(CustomUser.objects.count(), 1)
        customUser = CustomUser.objects.get(username=req_data["username"])
        self.assertEqual(customUser.first_name, req_data["first_name"])
        self.assertEqual(customUser.last_name, req_data["last_name"])
        self.assertEqual(customUser.email, req_data["email"])
        self.assertEqual(customUser.birth_date, req_data["birth_date"])
        self.assertEqual(customUser.gender, req_data["gender"])
        #self.assertEqual(customUser.image.url, "d")
        #self.assertEqual(os.path.join(settings.BASE_DIR, customUser.image.path), self.image_path)
        #self.assertEqual(customUser.image.name, "fff")
        #self.assertTrue(filecmp.cmp(os.path.join(settings.BASE_DIR, customUser.image.path), self.image_path))

        # test req method POST with invalid data
        # testing if existing username is accepted
        req_data = {
            "username" : "armin_gm", "password1" : "ain123456", "password2" : "ain123456", "first_name" : "rmin"
            , "last_name" : "behnamni", "email" : "inbehnamnia@gmail.com", "gender" : "female"
            , "birth_date" : datetime.date(year=1995, month=11, day=7), "is_host" : True, "image" : self.img
        }
        response = self.client.post(url, req_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CustomUser.objects.count(), 1)

        # test req method POST with invalid data
        req_data = {
            "username" : "armin_gm", "password1" : "armin123456", "password2" : "armin123457", "first_name" : "armin"
            , "last_name" : "behnamnia", "email" : "arminbehnamnia@gmail.com", "gender" : "male"
            , "birth_date" : datetime.date(year=1995, month=11, day=7), "image" : self.img
        }
        response = self.client.post(url, req_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CustomUser.objects.count(), 1)
        CustomUser.objects.all().delete()

    def test_host_registration(self):
        url = reverse('become_host')
        the_user = self.createUser()
        self.client.force_login(the_user)

        # test req method GET
        req = self.request_factory.get(url)
        req.user = the_user
        view = HostRegistration.as_view()
        response = view(req)
        self.assertEqual(response.status_code, 200)

        # test req method POST with empty data
        req = self.request_factory.post(url, data={})
        req.user = the_user
        view = HostRegistration.as_view()
        response = view(req)
        self.assertEqual(response.status_code, 200)

        # test req method POST with valid data
        req_data = {"user": the_user, "passport_pic": self.img,
                    "home_address": "Azadi St., Sharif University of Tech", "phone_number": "02144445555",
                    "city": "Tehran"}

        req = self.request_factory.post(url, data=req_data)
        req.user = the_user
        view = HostRegistration.as_view()
        response = view(req)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Host.objects.count(), 1)
        host = Host.objects.get(user=req_data["user"])
        self.assertEqual(host.home_address, req_data["home_address"])
        self.assertEqual(host.phone_number, req_data["phone_number"])
        self.assertEqual(host.city, req_data["city"])
        self.assertTrue(host.user.is_host)

    # def setup_request(self, request):
    #     request.user = self.u2
    #
    #     """Annotate a request object with a session"""
    #     middleware = SessionMiddleware()
    #     middleware.process_request(request)
    #     request.session.save()
    #
    #     """Annotate a request object with a messages"""
    #     middleware = MessageMiddleware()
    #     middleware.process_request(request)
    #     request.session.save()

    def test_editProfile(self):
        url = reverse("update_profile")
        the_user = self.createUser()
        the_user.set_password("armin1234")
        the_user.save()
        self.client.force_login(the_user)
        the_session = self.client.session

        # test req method GET
        req = self.request_factory.get(url)
        req.user = the_user
        view = EditProfile.as_view()
        response = view(req)
        self.assertEqual(response.status_code, 200)

        # test req method POST with empty data
        req = self.request_factory.post(url, data={})
        req.user = the_user
        view = EditProfile.as_view()
        response = view(req)
        self.assertEqual(response.status_code, 200)

    #   # test req method POST with valid data, changing user_form
        req_data = {"email": "gamemaking.ar@gmail.com", "gender":"female", "image":self.img2, "user_form":True}
        req = self.request_factory.post(url, data=req_data)
        req.user = the_user
        setattr(req, 'session', 'session')
        messages = FallbackStorage(req)
        setattr(req, '_messages', messages)
        view = EditProfile.as_view()
        response = view(req)
        self.assertEqual(response.status_code, 200)
        stored_user = CustomUser.objects.get(username=the_user.username)
        self.assertEqual(stored_user.gender, req_data["gender"])
        self.assertEqual(stored_user.email, req_data["email"])

        # test req method POST with valid data, changing password_form
        req_data = {"old_password": "armin1234", "new_password1":"xyzt4321tres", "new_password2":"xyzt4321tres"}
        req = self.request_factory.post(url, data=req_data)
        req.user = the_user
        setattr(req, 'session', the_session)
        messages = FallbackStorage(req)
        setattr(req, '_messages', messages)
        view = EditProfile.as_view()
        response = view(req)
        self.assertEqual(response.status_code, 200)
        stored_user = CustomUser.objects.get(username=the_user.username)
        self.assertTrue(stored_user.check_password(req_data["new_password1"]))
        the_user.set_password("armin1234")
        the_user.save()

        # test req method POST with invalid data, changing password_form, wrong old_password
        req_data_invalid = {"old_password": "armin4321", "new_password1":"xyzt4321tres", "new_password2":"xyzt4321tres"}
        req = self.request_factory.post(url, data=req_data_invalid)
        req.user = the_user
        setattr(req, 'session', the_session)
        messages = FallbackStorage(req)
        setattr(req, '_messages', messages)
        view = EditProfile.as_view()
        response = view(req)
        self.assertEqual(response.status_code, 200)
        stored_user = CustomUser.objects.get(username=the_user.username)
        self.assertTrue(stored_user.check_password(req_data["old_password"]))
        the_user.set_password("armin1234")
        the_user.save()

        # test req method POST with invalid data, changing password_form, new passwords mismatch
        req_data_invalid = {"old_password": "armin1234", "new_password1":"xyzt4321tres", "new_password2":"xyzt41tres"}
        req = self.request_factory.post(url, data=req_data_invalid)
        req.user = the_user
        setattr(req, 'session', the_session)
        messages = FallbackStorage(req)
        setattr(req, '_messages', messages)
        view = EditProfile.as_view()
        response = view(req)
        self.assertEqual(response.status_code, 200)
        stored_user = CustomUser.objects.get(username=the_user.username)
        self.assertTrue(stored_user.check_password(req_data["old_password"]))
