from django.contrib.auth.models import User
from django.test import TestCase

from logging_system.systems.models import System

from .models import Comment, Incident


class IncidentModelTest(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        # Create a test system
        self.system = System.objects.create(name="Test System")

        # Create an incident instance
        self.incident = Incident.objects.create(
            system=self.system,
            ip="192.168.1.1",
            tag=0,
            title="Test Incident",
            message="This is a test incident message",
            user=self.user,
        )

    def test_incident_creation(self):
        # Test if the incident is created properly
        self.assertEqual(self.incident.title, "Test Incident")
        self.assertEqual(self.incident.message, "This is a test incident message")
        self.assertEqual(self.incident.system.name, "Test System")
        self.assertEqual(self.incident.user.username, "testuser")
        self.assertEqual(self.incident.tag, 0)
        self.assertEqual(self.incident.ip, "192.168.1.1")

    def test_incident_str_method(self):
        # Test the __str__ method of the Incident model
        self.assertEqual(str(self.incident), "Test Incident")

    def test_default_tag(self):
        # Test if the default value of 'tag' field is 0 (System down)
        new_incident = Incident.objects.create(
            system=self.system,
            ip="192.168.1.2",
            title="New Incident",
            message="New incident message",
            user=self.user,
        )
        self.assertEqual(new_incident.tag, 0)

    def test_foreign_key_system(self):
        # Test if the system foreign key is set correctly
        self.assertEqual(self.incident.system, self.system)

    def test_foreign_key_user(self):
        # Test if the user foreign key is set correctly
        self.assertEqual(self.incident.user, self.user)


class CommentModelTest(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

        # Create a test system
        self.system = System.objects.create(name="Test System")

        # Create an incident instance
        self.incident = Incident.objects.create(
            system=self.system,
            ip="192.168.1.1",
            tag=0,
            title="Test Incident",
            message="This is a test incident message",
            user=self.user,
        )

        # Create a comment instance
        self.comment = Comment.objects.create(
            incident=self.incident,
            user=self.user,
            message="This is a test comment",
        )

    def test_comment_creation(self):
        # Test if the comment is created properly
        self.assertEqual(self.comment.message, "This is a test comment")
        self.assertEqual(self.comment.incident.title, "Test Incident")
        self.assertEqual(self.comment.user.username, "testuser")

    def test_comment_str_method(self):
        # Test the __str__ method of the Comment model
        self.assertEqual(str(self.comment), "This is a test comment")

    def test_foreign_key_incident(self):
        # Test if the incident foreign key is set correctly
        self.assertEqual(self.comment.incident, self.incident)

    def test_foreign_key_user(self):
        # Test if the user foreign key is set correctly
        self.assertEqual(self.comment.user, self.user)

    def test_comment_max_length(self):
        # Test if the message field's max length is respected
        long_message = "x" * 300
        comment = Comment.objects.create(
            incident=self.incident,
            user=self.user,
            message=long_message,
        )
        self.assertEqual(
            comment.message, long_message[:255]
        )  # Check that it's truncated
