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

        # test req method GET
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # test req method POST with empty data
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Host.objects.count(), 0)

        # creating user
        user_data = {
            "username" : "armin_gm", "password" : "armin1234", "first_name" : "armin", "last_name" : "behnamnia"
        , "email" : "arminbehnamnia@gmail.com", "gender" : "male"
        , "birth_date" : datetime.date(year=1995, month=11, day=7)
        , "image" : self.img, "is_host": False
        }
        the_user = CustomUser.objects.create(username="armin_gm", email="arminbehnamnia@gmail.com",
                                  last_name="armin", first_name="behnamnia",
                                  birth_date=datetime.date(year=1995, month=11, day=7), is_host=False, gender="male",
                                  image=self.img)
        the_user.set_password(user_data["password"])
        the_user.save()
        #CustomUser.save(the_user)
        #self.assertEqual(type(the_user).__name__, type(CustomUser()).__name__)
        #self.assertEqual(type(the_user), type(CustomUser(**user_data)))
        #the_user = authenticate(username=the_user.username, password=the_user.password)
        self.client.force_login(the_user)#, password=the_user.password)
        #req = self.request_factory.post(reverse("login"))
        #req.user=auth_user
        #self.client.post(req)
        #login(req, auth_user)
        #self.client.login(username=the_user.username, password=the_user.password)

        # test req method POST with valid data
        req_data = {"user": the_user, "passport_pic": self.img,
                    "home_address": "Azadi St., Sharif University of Tech", "phone_number": "02144445555",
                    "city": "Tehran"}
        response = self.client.post(url, req_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Host.objects.count(), 1)
        host = Host.objects.get(user=req_data["user"])
        self.assertEqual(host.home_address, req_data["home_address"])
        self.assertEqual(host.phone_number, req_data["phone_number"])
        self.assertEqual(host.city, req_data["city"])
        self.assertTrue(host.user.is_host)
        #self.assertTrue(filecmp.cmp(os.path.join(settings.BASE_DIR, host.passport_pic.path), self.image_path))

        # test req method POST with invalid data
        req_data = {"user": the_user, "passport_pic": self.img,
                    "home_address": "Azadi St., Sharif University of Tech",
                    "city": "Tehran"}
        response = self.client.post(url, req_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Host.objects.count(), 1)
        CustomUser.objects.all().delete()
        Host.objects.all().delete()

    def test_editProfile(self):
        url = reverse("update_profile")
        # creating user
        user_data = {
            "username" : "armin_gm", "password" : "armin1234", "first_name" : "armin", "last_name" : "behnamnia"
        , "email" : "arminbehnamnia@gmail.com", "gender" : "male"
        , "birth_date" : datetime.date(year=1995, month=11, day=7)
        , "image" : self.img, "is_host": False
        }
        the_user = CustomUser.objects.create(username="armin_gm", email="arminbehnamnia@gmail.com",
                                  last_name="armin", first_name="behnamnia",
                                  birth_date=datetime.date(year=1995, month=11, day=7), is_host=False, gender="male",
                                  image=self.img)
        the_user.set_password(user_data["password"])
        the_user.save()
        #CustomUser.save(the_user)
        #self.assertEqual(type(the_user).__name__, type(CustomUser()).__name__)
        #self.assertEqual(type(the_user), type(CustomUser(**user_data)))
        #the_user = authenticate(username=the_user.username, password=the_user.password)
        self.client.force_login(the_user)#, password=the_user.password)

        # test req method GET
        req = self.request_factory.get(url)
        req.user = the_user
        view = EditProfile.as_view()
        response = view(req)
        self.assertEqual(response.status_code, 200)

        # test req method POST with empty data

        req = self.request_factory.post(url, {})
        req.user = the_user
        view = EditProfile.as_view()
        response = view(req)
        self.assertEqual(response.status_code, 200)

        # test req method POST with valid data, changing user_form
        stored_user = CustomUser.objects.get(username=the_user.username)
        self.assertEqual(stored_user.gender, user_data["gender"])
        self.assertEqual(stored_user.email, user_data["email"])
        change_data = {"email": "gamemaking.ar@gmail.com", "gender":"female", "image":self.img2, "user_form":True}
        req = self.request_factory.post(url, change_data)
        req.user = the_user
        view = EditProfile.as_view()
        response = view(req)
        self.assertEqual(response.status_code, 302)
        stored_user = CustomUser.objects.get(username=the_user.username)
        self.assertEqual(stored_user.gender, change_data["gender"])
        self.assertEqual(stored_user.email, change_data["email"])

        # test req method POST with valid data, changing password_form
        change_data = {"old_password": "armin1234", "new_password1":"armin4321", "new_password2":"armin4321"}
        req = self.request_factory.post(url, change_data)
        req.user = the_user
        view = EditProfile.as_view()
        response = view(req)
        self.assertEqual(response.status_code, 200)
        stored_user = CustomUser.objects.get(username=the_user.username)
        self.assertTrue(stored_user.check_password(change_data["old_password"]))
        #self.assertEqual(stored_user.gender, change_data["gender"])
        #self.assertEqual(stored_user.email, change_data["email"])

