from django.test import TestCase
from registration.models import CustomUser, Host
import datetime
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from Code.settings import BASE_DIR
import filecmp


class TestRegistrationModels(TestCase):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(BASE_DIR, "testMedia/image1.jpg")

    def setUp(self):
        self.img = SimpleUploadedFile(name='test_image.jpg', content=open(self.image_path, 'rb').read(),
                                      content_type='image/jpeg')

    def testCustomUser(self):
        exp_data = {"username": "armin_gm", "password": "armin1234", "email": "arminbehnamnia@gmail.com",
                    "last_name": "armin", "first_name": "behnamnia",
                    "birth_date": datetime.date(year=1995, month=11, day=7), "is_host": True, "gender": "female",
                    "image": self.img}
        CustomUser.objects.create(username="armin_gm", password="armin1234", email="arminbehnamnia@gmail.com",
                                  last_name="armin", first_name="behnamnia",
                                  birth_date=datetime.date(year=1995, month=11, day=7), is_host=True, gender="female",
                                  image=self.img)
        self.assertEqual(CustomUser.objects.count(), 1)
        customUser = CustomUser.objects.get(username=exp_data["username"])
        self.assertEqual(customUser.password, exp_data["password"])
        self.assertEqual(customUser.first_name, exp_data["first_name"])
        self.assertEqual(customUser.last_name, exp_data["last_name"])
        self.assertEqual(customUser.email, exp_data["email"])
        self.assertEqual(customUser.birth_date, exp_data["birth_date"])
        self.assertEqual(customUser.gender, exp_data["gender"])
        self.assertEqual(customUser.is_host, exp_data["is_host"])
        self.assertTrue(filecmp.cmp(os.path.join(BASE_DIR, customUser.image.path), self.image_path))

    def testHost(self):
        CustomUser.objects.create(username="armin_gm", password="armin1234", email="arminbehnamnia@gmail.com",
                                  last_name="armin", first_name="behnamnia",
                                  birth_date=datetime.date(year=1995, month=11, day=7), is_host=False, gender="female",
                                  image=self.img)
        customUser = CustomUser.objects.get(username="armin_gm")

        exp_data = {"user": customUser, "passport_pic": self.img,
                    "home_address": "Azadi St., Sharif University of Tech",
                    "phone_number": "02144445555", "city": "Tehran"}
        Host.objects.create(user=customUser, passport_pic=self.img, home_address="Azadi St., Sharif University of Tech",
                            phone_number="02144445555", city="Tehran")
        self.assertEqual(Host.objects.count(), 1)
        host = Host.objects.get(user=customUser)
        self.assertTrue(filecmp.cmp(os.path.join(BASE_DIR, host.passport_pic.path), self.image_path))
        self.assertEqual(host.home_address, exp_data["home_address"])
        self.assertEqual(host.phone_number, exp_data["phone_number"])
        self.assertEqual(host.city, exp_data["city"])
