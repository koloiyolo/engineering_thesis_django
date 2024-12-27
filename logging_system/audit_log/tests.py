from django.test import TestCase
from django.contrib.auth.models import User
from .models import AuditLog
from django.utils import timezone

class AuditLogTestCase(TestCase):
    
    def setUp(self):
        # This method will run before each test.
        # Create a test user for the ForeignKey relationship.
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.now = timezone.now() 

    def test_create_audit_log(self):
        # Test creating and saving an AuditLog instance.
        audit_log = AuditLog.objects.create(
            user=self.user,
            message="Test message for audit log"
        )

        self.assertEqual(AuditLog.objects.count(), 1)
        self.assertEqual(audit_log.user, self.user)
        self.assertEqual(audit_log.message, "Test message for audit log")
        self.assertTrue(audit_log.datetime <= timezone.now())
    
    def test_user_can_be_null(self):
        
        # Test that user can be set to null.
        
        audit_log = AuditLog.objects.create(
            user=None,
            message="Test message with no user"
        )

        self.assertIsNone(audit_log.user)
    
    def test_message_max_length(self):
        # Test that the message field does not exceed the max length (255 characters).
        long_message = "A" * 256  
        audit_log = AuditLog.objects.create(
            user=self.user,
            message=long_message
        )
        self.assertEqual(len(audit_log.message), 255)
    
    def test_create_audit_log_without_message(self):
        # Test creating an AuditLog without a message.
        audit_log = AuditLog.objects.create(
            user=self.user,
            message=""  
        )

        self.assertEqual(audit_log.message, "")

    def test_auto_now_datetime(self):
        # Test that the `datetime` field is automatically set.
        audit_log = AuditLog.objects.create(
            user=self.user,
            message="Test message with auto_now"
        )

        self.assertIsNotNone(audit_log.datetime)
        self.assertTrue(audit_log.datetime <= timezone.now()) 
