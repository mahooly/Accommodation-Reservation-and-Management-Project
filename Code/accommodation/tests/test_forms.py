from django.test import TestCase
from django.test import TestCase
import datetime
from Code.accommodation.forms import CustomUserCreationForm, CustomUserChangeForm
from django.core.files.uploadedfile import SimpleUploadedFile
import os
import logging


class TestRegistrationForm(TestCase):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(BASE_DIR, "testMedia/image1.jpg")
    # Get an instance of a logger
    logger = logging.getLogger(__name__)

    def setUp(self):
        self.img = SimpleUploadedFile(name='test_image.jpg', content=open(self.image_path, 'rb').read(),
                                            content_type='image/jpeg')

    def test_registration_form(self):

        invalid_data = {
            "username" : "armin_gm", "password1" : "armin123456", "password2" : "armin123456", "first_name" : "armin", "last_name" : "behnamnia"
        , "email" : "arminbehnamniagmail.com", "gender" : "male"
        , "birth_date" : datetime.date(year=1995, month=11, day=7)
        , "is_host" : True, "image" : self.img
        }
        form = CustomUserCreationForm(data=invalid_data)
        form.is_valid()
        self.assertTrue(form.errors)
        invalid_data = {
            "username" : "armin_gm", "password1" : "1234", "password2" : "1234", "first_name" : "armin", "last_name" : "behnamnia"
        , "email" : "arminbehnamnia@gmail.com", "gender" : "male"
        , "birth_date" : datetime.date(year=1995, month=11, day=7)
        , "is_host" : True, "image" : self.img
        }
        form = CustomUserCreationForm(data=invalid_data)
        form.is_valid()
        self.assertTrue(form.errors)
        invalid_data = {
            "username" : "armin_gm", "password1" : "armin123456", "password2" : "armin123457", "first_name" : "armin", "last_name" : "behnamnia"
        , "email" : "arminbehnamnia@gmail.com", "gender" : "male"
        , "birth_date" : datetime.date(year=1995, month=11, day=7)
        , "is_host" : True, "image" : self.img
        }
        form = CustomUserCreationForm(data=invalid_data)
        form.is_valid()
        self.assertTrue(form.errors)

        valid_data = {
            "username" : "armin_gm", "password1" : "armin12345678", "password2" : "armin12345678", "first_name" : "armin", "last_name" : "behnamnia"
        , "email" : "arminbehnamnia@gmail.com", "gender" : "male"
        , "birth_date" : datetime.date(year=1995, month=11, day=7)
        , "is_host" : True, "image" : self.img
        }
        form = CustomUserCreationForm(data=valid_data)
        form.is_valid()
        self.assertFalse(form.errors)
        # !!Username does not have any constraints
    def test_change_form(self):

        invalid_data = {"email" : "arminbehnamniagmail.com"
            , "gender" : "male", "image" : self.img
        }
        form = CustomUserChangeForm(data=invalid_data)
        form.is_valid()
        self.assertTrue(form.errors)
        # invalid_data = {"email" : "arminbehnamnia@gmail.com"
        #     , "gender" : "mane", "image" : self.img
        # }
        # form = CustomUserChangeForm(data=invalid_data)
        # form.is_valid()
        # self.assertTrue(form.errors)
        valid_data = {"email" : "arminbehnamnia@gmail.com"
            , "gender" : "male", "image" : self.img
        }
        form = CustomUserChangeForm(data=valid_data)
        form.is_valid()
        self.assertFalse(form.errors)
# Create your tests here.
