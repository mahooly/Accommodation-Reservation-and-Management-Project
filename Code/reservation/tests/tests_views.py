from django.test import TestCase, Client, RequestFactory
from django.contrib.messages.storage.fallback import FallbackStorage
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from registration.models import CustomUser, Host
from accommodation.views import CreateAccommodationView, AccommodationDetailView
from accommodation.models import Amenity, Accommodation
from accommodation.forms import AccommodationCreationForm, FileFieldForm
from ..views import MakeReservation
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
    
    def createAccommodation(self, host):
        a1 = self.createAmenity(1)
        a2 = self.createAmenity(2)
        a1.save()
        a2.save()
        the_acc = Accommodation.objects.create(owner=the_host, accommodation_type='هتل', title="Model_Ghoo", description="A decent luxury hotel.", province="Tehran"
                                                city='Tehran', address='1234', email='armin@gmail.com', phone='02122334455', amenity=[a1, a2])
        the_acc.save()
        return the_acc
    
    def addRooms(self, acc, how_many):
        a1 = self.createAmenity(3)
        a2 = self.createAmenity(4)
        a1.save()
        a2.save()

        the_room = Room.objects.create(accommodation=acc, amenity=[a1, a2], description='hi hi hi', bed_type='Single', number_of_guests=1, image=self.img2, price=123)
        the_room.save()
        for i in range(how_many):
                RoomInfo.objects.create(room=the_room)
        return the_room
        
    def searchForRoom(self, user, acc):
        req = {'user':user, 'form': {'check_in': '12122019', 'check_out': '14122019', 'price':'100-200'}}
        view = AccommodationDetailView.as_view()
        response = view(req, pk=acc.pk)
        print(response)
        return response

    
    def test_reserve(self):
        # url = reverse("create_accommodation")
        the_host = self.createHost()
        the_user = the_host.user
        the_user.set_password("armin1234")
        the_user.save()
        self.client.force_login(the_user)
        acc = self.createAccommodation(the_host)
        room = self.addRooms(acc, 3)
        # self.searchForRoom(the_user, acc)
        req = {}
        view = MakeReservation(req, rid=room.pk)



