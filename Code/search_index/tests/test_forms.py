from django.test import TestCase
from ..forms import FilterForm, LocationSearchForm


class TestSearchIndexForm(TestCase):
    def test_locationSearchForm(self):
        valid_data = {"expression": "Sharif University"}
        form = LocationSearchForm(data=valid_data)
        form.is_valid()
        self.assertFalse(form.errors)

    def test_filterForm(self):
        valid_data = {"province": "Tehran", "hotel": True, "motel": False, "house": True, "city": "Tehran"}
        form = FilterForm(data=valid_data)
        form.is_valid()
        self.assertFalse(form.errors)

        invalid_data = {"province": "یه توپ دارم قلقلیه سرخ و سفید و آبیه میزنم زمین هوا میره نمیدونی تا کجا میره!",
                        "hotel": True, "motel": False, "house": True, "city": "Tehran"}
        form = FilterForm(data=invalid_data)
        form.is_valid()
        self.assertTrue(form.errors)

        # !!Username does not have any constraints
