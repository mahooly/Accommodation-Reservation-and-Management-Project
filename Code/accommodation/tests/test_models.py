from django.test import TestCase
from ..models import Amenity, Accommodation, Room, Image, RoomInfo
import datetime
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from registration.models import Host, CustomUser


class TestAccommodationModels(TestCase):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(BASE_DIR, "testMedia/image1.jpg")

    def setUp(self):
        self.img = SimpleUploadedFile(name='test_image.jpg', content=open(self.image_path, 'rb').read(),
                                      content_type='image/jpeg')

    def createAmenity(self):
        amenity = Amenity.objects.create(name="Couch", label="Red")
        amenity.save()
        return amenity

    def testAmenity(self):
        am_count = Amenity.objects.count()
        exp_data = {"name": "Couch", "label": "Red"}
        amenity = Amenity.objects.create(name="Couch", label="Red")
        amenity.save()
        self.assertEqual(Amenity.objects.count(), am_count + 1)
        self.assertEqual(amenity.name, exp_data["name"])
        self.assertEqual(amenity.label, exp_data["label"])

    def createHost(self):
        the_user = CustomUser.objects.create(username="armin_gm", email="arminbehnamnia@gmail.com",
                                             last_name="armin", first_name="behnamnia",
                                             birth_date=datetime.date(year=1995, month=11, day=7), is_host=False,
                                             gender="male",
                                             image=self.img)
        the_user.save()
        the_host = Host.objects.create(user=the_user, passport_pic=self.img,
                                       home_address="Azadi St., Sharif University of Tech", phone_number="02144445555",
                                       city="Tehran")
        the_host.save()
        return the_host

    def createAccommodation(self):
        the_host = self.createHost()
        the_amenity = self.createAmenity()
        the_accommodation = Accommodation.objects.create(owner=the_host, title="Model_Ghoo",
                                                         description="A decent luxury hotel.",
                                                         accommodation_type="هتل", province="Tehran", city="Tehran",
                                                         address="1234",
                                                         phone="02144239859", email="armin@gmail.com")
        the_accommodation.amenity.add(the_amenity)
        the_accommodation.save()
        return the_accommodation

    def testAccommodation(self):
        acc_count = Accommodation.objects.count()
        the_host = self.createHost()
        the_amenity = self.createAmenity()
        exp_data = {"owner": the_host, "title": "Model_Ghoo", "description": "A decent luxury hotel.",
                    "accommodation_type": "هتل", "province": "Tehran", "city": "Tehran", "address": "1234",
                    "phone": "02144239859", "email": "armin@gmail.com", "amenity": the_amenity}
        the_accommodation = Accommodation.objects.create(owner=the_host, title="Model_Ghoo",
                                                         description="A decent luxury hotel.",
                                                         accommodation_type="هتل", province="Tehran", city="Tehran",
                                                         address="1234",
                                                         phone="02144239859", email="armin@gmail.com")
        the_accommodation.amenity.add(the_amenity)
        the_accommodation.save()
        self.assertEqual(Accommodation.objects.count(), acc_count + 1)
        self.assertEqual(the_accommodation.owner, exp_data["owner"])
        self.assertEqual(the_accommodation.title, exp_data["title"])
        self.assertEqual(the_accommodation.description, exp_data["description"])
        self.assertEqual(the_accommodation.province, exp_data["province"])
        self.assertEqual(the_accommodation.address, exp_data["address"])
        self.assertEqual(the_accommodation.phone, exp_data["phone"])
        self.assertEqual(the_accommodation.email, exp_data["email"])
        self.assertEqual(the_accommodation.amenity.all().count(), 1)
        self.assertEqual(the_accommodation.amenity.all()[0], exp_data["amenity"])

        # testing accommodation model methods
        data_1 = {"description": "a convenient room.",
                  "bed_type": "Single", "number_of_guests": 4, "image": self.img}
        data_2 = {"description": "a double convenient room.",
                  "bed_type": "Double", "number_of_guests": 6, "image": self.img}
        data_3 = {"description": "a twin convenient room.",
                  "bed_type": "Twin", "number_of_guests": 5, "image": self.img}

        the_room_1 = self.createRoomFromAccomodation(the_accommodation, data_1)
        the_room_1.amenity.add(the_amenity)
        the_room_1.save()
        RoomInfo.objects.create(room=the_room_1)
        the_room_2 = self.createRoomFromAccomodation(the_accommodation, data_2)
        the_room_2.amenity.add(the_amenity)
        the_room_2.save()
        RoomInfo.objects.create(room=the_room_2)
        the_room_3 = self.createRoomFromAccomodation(the_accommodation, data_3)
        the_room_3.amenity.add(the_amenity)
        the_room_3.save()
        RoomInfo.objects.create(room=the_room_3)

        self.assertEqual(the_accommodation.rooms, 3)
        self.assertEqual(the_accommodation.single_beds, 1)
        self.assertEqual(the_accommodation.double_beds, 1)
        self.assertEqual(the_accommodation.twin_beds, 1)
        self.assertEqual(the_accommodation.guests, the_room_1.number_of_guests + the_room_2.number_of_guests +
                         the_room_3.number_of_guests)

    def createRoomFromAccomodation(self, accommodation, data):
        the_room = Room.objects.create(accommodation=accommodation, description=data["description"],
                                       bed_type=data["bed_type"], number_of_guests=data["number_of_guests"],
                                       image=data["image"])
        the_room.save()
        return the_room

    def testRoom(self):
        r_count = Room.objects.count()
        the_accommodation = self.createAccommodation()
        the_amenity = the_accommodation.amenity.all()[0]
        exp_data = {"accommodation": the_accommodation, "amenity": the_amenity, "description": "a convenient room.",
                    "bed_type": "Single", "number_of_guests": 4, "image": self.img, "how_many": 2}
        the_room = Room.objects.create(accommodation=the_accommodation, description="a convenient room.",
                                       bed_type="Single", number_of_guests=4, image=self.img)
        the_room.amenity.add(the_amenity)
        the_room.save()
        self.assertEqual(Room.objects.count(), r_count + 1)
        self.assertEqual(the_room.accommodation, exp_data["accommodation"])
        self.assertEqual(the_room.amenity.count(), 1)
        self.assertEqual(the_room.amenity.all()[0], exp_data["amenity"])
        self.assertEqual(the_room.description, exp_data["description"])
        self.assertEqual(the_room.bed_type, exp_data["bed_type"])
        self.assertEqual(the_room.number_of_guests, exp_data["number_of_guests"])

    def testImage(self):
        the_accommodation = self.createAccommodation()
        exp_data = {"accommodation": the_accommodation, "image": self.img}
        the_image = Image.objects.create(accommodation=the_accommodation, image=self.img)
        the_image.save()
        self.assertEqual(Image.objects.count(), 1)
        self.assertEqual(the_image.accommodation, exp_data["accommodation"])
