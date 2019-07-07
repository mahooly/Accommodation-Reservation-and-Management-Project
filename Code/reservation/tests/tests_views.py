from django.contrib.messages import get_messages
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from registration.models import CustomUser, Host
from accommodation.views import AccommodationDetailView
from accommodation.models import Amenity, Accommodation, Room, RoomInfo
from reservation.models import Reservation
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
        the_acc = Accommodation.objects.create(owner=host, accommodation_type='هتل', title="Model_Ghoo",
                                               description="A decent luxury hotel.", province="Tehran",
                                               city='Tehran', address='1234', email='armin@gmail.com',
                                               phone='02122334455')
        the_acc.amenity.add(a1)
        the_acc.amenity.add(a2)
        the_acc.save()
        return the_acc

    def addRooms(self, acc, how_many):
        a1 = self.createAmenity(3)
        a2 = self.createAmenity(4)
        a1.save()
        a2.save()

        the_room = Room.objects.create(accommodation=acc, description='hi hi hi', bed_type='Single',
                                       number_of_guests=1, image=self.img2, price=123)
        the_room.amenity.add(a1)
        the_room.amenity.add(a2)
        the_room.save()
        for i in range(how_many):
            RoomInfo.objects.create(room=the_room)
        return the_room

    def searchForRoom(self, user, acc):
        req = {'user': user, 'form': {'check_in': '12122019', 'check_out': '14122019', 'price': '100-200'}}
        view = AccommodationDetailView.as_view()
        response = view(req, pk=acc.pk)
        return response

    def test_reserve(self):
        the_host = self.createHost()
        the_user = the_host.user
        the_user.set_password("armin1234")
        the_user.save()
        self.client.force_login(the_user)
        acc = self.createAccommodation(the_host)
        room = self.addRooms(acc, 3)
        response = self.client.post(reverse('make_reservation', kwargs={'rid': room.id}),
                                    {'check_in': '07/12/2019', 'check_out': '07/15/2019',
                                     'how_many': 3})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Reservation.objects.count(), 1)
        reservation = Reservation.objects.get(reserver=the_user)
        self.assertEqual(reservation.check_in, datetime.date(2019, 7, 12))
        self.assertEqual(reservation.check_out, datetime.date(2019, 7, 15))

        # try to reserve again

        response2 = self.client.post(reverse('make_reservation', kwargs={'rid': room.id}),
                                     {'check_in': '07/12/2019', 'check_out': '07/14/2019',
                                      'how_many': 1})
        messages = list(get_messages(response2.wsgi_request))
        self.assertEqual(len(messages), 2)
        self.assertEqual(str(messages[1]),
                         'در رزرو کردن اتاق مشکلی پیش آمده است. لطفاً دوباره تلاش کنید. به این تعداد اتاق خالی وجود ندارد.')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Reservation.objects.count(), 1)
        reservation = Reservation.objects.get(reserver=the_user)
        self.assertEqual(reservation.check_out, datetime.date(2019, 7, 15))
