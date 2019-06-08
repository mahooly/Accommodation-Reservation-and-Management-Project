from django.test import TestCase, Client, RequestFactory
from django.contrib.messages.storage.fallback import FallbackStorage
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from registration.models import CustomUser, Host
from ..views import CreateAccommodationView
from ..models import Amenity, Accommodation
from ..forms import AccommodationCreationForm, FileFieldForm
import os
import datetime


class TestAccommocationView(TestCase):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(BASE_DIR, "testMedia/image1.jpg")
    image_path2 = os.path.join(BASE_DIR, "testMedia/image2.jpg")
    request_factory = RequestFactory()

    def setUp(self):
        self.client = Client()
        self.img_content = open(self.image_path, 'r')
        self.img = SimpleUploadedFile(name='test_image.jpg', content=open(self.image_path, 'rb').read(),
                                      content_type='image/jpeg')
        self.img2 = SimpleUploadedFile(name='test_image2.jpg', content=open(self.image_path2, 'rb').read(),
                                       content_type='image/jpeg')

    def createHost(self):
        the_user = CustomUser.objects.create(username="armin_gm", email="arminbehnamnia@gmail.com",
                                             last_name="armin", first_name="behnamnia",
                                             birth_date=datetime.date(year=1995, month=11, day=7), is_host=False,
                                             gender="male",
                                             image=self.img)
        the_user.is_host = True
        the_user.save()
        the_host = Host.objects.create(user=the_user, passport_pic=self.img,
                                       home_address="Azadi St., Sharif University of Tech", phone_number="02144445555",
                                       city="Tehran")
        the_host.save()
        return the_host

    def createAmenity(self, index):
        amenity = Amenity.objects.create(name="Couch" + str(index), label="Red")
        amenity.save()
        return amenity

    def test_createAccommodationView(self):
        url = reverse("create_accommodation")
        the_host = self.createHost()
        the_user = the_host.user
        the_user.set_password("armin1234")
        the_user.save()
        self.client.force_login(the_user)
        the_session = self.client.session

        # test req method GET
        req = self.request_factory.get(url)
        req.user = the_user
        view = CreateAccommodationView.as_view()
        response = view(req)
        self.assertEqual(response.status_code, 200)

        # test req method POST with empty data
        req = self.request_factory.post(url, data={})
        req.user = the_user
        view = CreateAccommodationView.as_view()
        response = view(req)
        self.assertEqual(response.status_code, 200)

        # # test req mothod POST with valid data
        # the_amenity1 = self.createAmenity(1)
        # the_amenity2 = self.createAmenity(2)
        # the_amenity1.save()
        # the_amenity2.save()
        #
        # req_data = {'accommodation_type': "هتل", 'title':"Model_Ghoo", 'description': "A decent luxury hotel.",
        #               'province':"Tehran", 'city':"Tehran", 'address':"1234", 'email':"armin@gmail.com",
        #               'phone':"02144239859", 'amenity':[the_amenity1, the_amenity2]}
        # content_type = "multipart/form-data; boundary=------------------------1493314174182091246926147632"
        # req = self.request_factory.post(url, data=req_data, content_type=content_type)
        # req.FILES['image'] = self.img_content
        # req.user = the_user
        # setattr(req, 'session', the_session)
        # messages = FallbackStorage(req)
        # setattr(req, '_messages', messages)
        # view = CreateAccommodationView.as_view()
        # response = view(req)
        # form = AccommodationCreationForm(data=req_data)
        # form.is_valid()
        # self.assertFalse(form.errors)
        # image_form = FileFieldForm(req.POST, req.FILES)
        # image_form.is_valid()
        # self.assertFalse(image_form.errors)
        #
        # self.assertEqual(response.status_code, 302)
        # self.assertEqual(Accommodation.objects.count(), 1)
        # test req mothod POST with valid data
        # the_amenity1 = self.createAmenity(1)
        # the_amenity2 = self.createAmenity(2)
        # the_amenity1.save()
        # the_amenity2.save()
        #
        # req_data = {'accommodation_type': "هتل", 'title': "Model_Ghoo", 'description': "A decent luxury hotel.",
        #             'province': "Tehran", 'city': "Tehran", 'address': "1234", 'email': "armin@gmail.com",
        #             'phone': "02144239859", 'amenity': [the_amenity1, the_amenity2], 'image': self.img}
        # content_type = "multipart/form-data; boundary=------------------------1493314174182091246926147632"
        # req = self.request_factory.post(url, data=req_data, content_type=content_type)
        # # req.FILES['image'] = [self.img_content]
        # req.user = the_user
        # setattr(req, 'session', the_session)
        # messages = FallbackStorage(req)
        # setattr(req, '_messages', messages)
        # view = CreateAccommodationView.as_view()
        # response = view(req)
        # form = AccommodationCreationForm(data=req_data)
        # form.is_valid()
        # self.assertFalse(form.errors)
        # image_form = FileFieldForm(files={'image': self.img_content})
        # image_form.is_valid()
        # self.assertFalse(image_form.errors)
        #
        # self.assertEqual(response.status_code, 302)
        # self.assertEqual(Accommodation.objects.count(), 1)

        def tearDown(self) -> None:
            self.img_content.close()
