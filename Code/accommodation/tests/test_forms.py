from django.test import TestCase
from django.test import TestCase
import datetime
from django.core.files.uploadedfile import SimpleUploadedFile
import os
import logging
from ..forms import AccommodationCreationForm, RoomCreationForm
from ..models import Amenity, Accommodation


class TestRegistrationForm(TestCase):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(BASE_DIR, "testMedia/image1.jpg")
    # Get an instance of a logger
    logger = logging.getLogger(__name__)

    def createAmenity(self, index):
        amenity = Amenity.objects.create(name="Couch" + str(index), label="Red")
        amenity.save()
        return amenity

    def setUp(self):
        self.img = SimpleUploadedFile(name='test_image.jpg', content=open(self.image_path, 'rb').read(),
                                      content_type='image/jpeg')

    def test_AccommodationCreationForm(self):
        the_amenity1 = self.createAmenity(1)
        the_amenity2 = self.createAmenity(2)
        valid_data = {'accommodation_type': "هتل", 'title': "Model_Ghoo", 'description': "A decent luxury hotel.",
                      'province': "Tehran", 'city': "Tehran", 'address': "1234", 'email': "armin@gmail.com",
                      'phone': "02144239859", 'amenity': [the_amenity1, the_amenity2]}

        form = AccommodationCreationForm(data=valid_data)
        form.is_valid()
        self.assertFalse(form.errors)

    def test_RoomCreationForm(self):
        the_amenity1 = self.createAmenity(1)
        the_amenity2 = self.createAmenity(2)

        # using amenities not assigned for rooms, invalid data
        invalid_data = {'how_many': 5, 'bed_type': "Double", 'number_of_guests': 7,
                        'amenity': [the_amenity1, the_amenity2],
                        'description': 'a nice double room with great view over sea', 'image': self.img}
        form = RoomCreationForm(data=invalid_data)
        form.is_valid()
        self.assertTrue(form.errors)

        # valid data
        the_amenity1.label = "room"
        the_amenity2.label = "room"
        the_amenity1.save()
        the_amenity2.save()

        valid_data = {'how_many': 5, 'bed_type': "Double", 'number_of_guests': 7,
                      'amenity': [the_amenity1, the_amenity2],
                      'description': 'a nice double room with great view over sea', 'price': 10000}
        form = RoomCreationForm(data=valid_data, files={'image': self.img})
        form.is_valid()
        self.assertFalse(form.errors)
