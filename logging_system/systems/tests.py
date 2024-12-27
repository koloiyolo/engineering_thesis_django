from django.test import TestCase
from .models import System, Ping
from locations.models import Location

class SystemModelTest(TestCase):

    def setUp(self):
        # Create a test Location instance
        self.location = Location.objects.create(
            name="Main Office",
            town="New York",
            address="123 Main St",
            room="101",
            notes="First-floor office"
        )

        # Create a test System instance
        self.system = System.objects.create(
            name="Test Device",
            ip="192.168.0.1",
            system_type=0,  # Device
            port="8080",
            to_ping=True,
            last_ping="2024-12-01",
            last_log="2024-12-01 12:00:00",
            d_count=10,
            email_notify=True,
            location=self.location,  # ForeignKey to Location
            service_type="Web Service",
            model="ABC123",
            notes="Test system note"
        )

    def test_system_creation(self):
        # Test if the System instance is created correctly
        self.assertEqual(self.system.name, "Test Device")
        self.assertEqual(self.system.ip, "192.168.0.1")
        self.assertEqual(self.system.system_type, 0)  # Device
        self.assertEqual(self.system.port, "8080")
        self.assertTrue(self.system.to_ping)
        self.assertEqual(self.system.last_ping, "2024-12-01")
        self.assertEqual(self.system.last_log, "2024-12-01 12:00:00")
        self.assertEqual(self.system.d_count, 10)
        self.assertTrue(self.system.email_notify)
        self.assertEqual(self.system.location.name, "Main Office")  # Verify Location
        self.assertEqual(self.system.service_type, "Web Service")
        self.assertEqual(self.system.model, "ABC123")
        self.assertEqual(self.system.notes, "Test system note")

    def test_system_str_method(self):
        # Test the __str__ method of the System model
        self.assertEqual(str(self.system), "Test Device")

    def test_default_to_ping(self):
        # Test if the default value of 'to_ping' is True
        new_system = System.objects.create(
            name="New Device",
            ip="192.168.0.2",
            system_type=0,  # Device
            port="8081",
        )
        self.assertTrue(new_system.to_ping)

    def test_foreign_key_location(self):
        # Test the foreign key relationship with Location
        self.assertEqual(self.system.location.name, "Main Office")

    def test_system_location_null(self):
        # Test creating a system without a location (null foreign key)
        system_no_location = System.objects.create(
            name="System without location",
            ip="192.168.1.1",
            system_type=0,  # Device
            port="8080",
            to_ping=True,
            last_ping="2024-12-01",
            last_log="2024-12-01 12:00:00",
            d_count=5,
            email_notify=False,
            location=None,  # No location provided
        )
        self.assertIsNone(system_no_location.location)

    def test_system_location_blank(self):
        # Test creating a system with a blank location (null allowed)
        location_blank = Location.objects.create(
            name="Location without details",
            town=None,
            address=None,
            room=None,
            notes=None
        )
        system_blank_location = System.objects.create(
            name="System with blank location",
            ip="192.168.1.2",
            system_type=1,  # Computer
            port="8082",
            to_ping=True,
            last_ping="2024-12-01",
            last_log="2024-12-01 12:00:00",
            d_count=0,
            email_notify=True,
            location=location_blank,  # Set blank location
        )
        self.assertEqual(system_blank_location.location.name, "Location without details")
        self.assertIsNone(system_blank_location.location.town)
        self.assertIsNone(system_blank_location.location.address)
        self.assertIsNone(system_blank_location.location.room)
        self.assertIsNone(system_blank_location.location.notes)

