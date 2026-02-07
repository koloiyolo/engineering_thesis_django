from django.test import TestCase
from .models import Location


class LocationModelTest(TestCase):
    def setUp(self):
        # Create a Location instance
        self.location = Location.objects.create(
            name="Main Office",
            town="New York",
            address="123 Main St",
            room="101",
            notes="First-floor office",
        )

    def test_location_creation(self):
        # Test if the Location instance is created correctly
        self.assertEqual(self.location.name, "Main Office")
        self.assertEqual(self.location.town, "New York")
        self.assertEqual(self.location.address, "123 Main St")
        self.assertEqual(self.location.room, "101")
        self.assertEqual(self.location.notes, "First-floor office")

    def test_location_str_method(self):
        # Test the __str__ method of the Location model
        self.assertEqual(str(self.location), "Main Office")

    def test_location_with_optional_fields(self):
        # Test creation of Location with optional fields (town, address, room, notes)
        location = Location.objects.create(name="Warehouse")
        self.assertEqual(location.name, "Warehouse")
        self.assertIsNone(location.town)
        self.assertIsNone(location.address)
        self.assertIsNone(location.room)
        self.assertIsNone(location.notes)

    def test_location_with_blank_fields(self):
        # Test creation of Location with blank fields
        location = Location.objects.create(name="Server Room", room="B23", notes="")
        self.assertEqual(location.name, "Server Room")
        self.assertEqual(location.room, "B23")
        self.assertEqual(location.notes, "")

    def test_max_length_name(self):
        # Test if name field exceeds the max_length
        long_name = "x" * 51  # Name length is 51, which exceeds max_length of 50
        location = Location.objects.create(name=long_name)
        self.assertEqual(location.name, "x" * 50)

    def test_max_length_address(self):
        # Test if address field exceeds the max_length
        long_address = (
            "x" * 101
        )  # Address length is 101, which exceeds max_length of 100
        location = Location.objects.create(
            name="Another Location", address=long_address
        )
        self.assertEqual(location.address, "x" * 100)
