from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import Notification, NotificationService

class NotificationTests(TestCase):
    def test_user_isolation_and_read_flow(self):
        User = get_user_model()
        user = User.objects.create_user(email="notify@example.com", password="x", name="Notify")
        item = NotificationService.create(user, title="Task due", message="Your task is due.")
        self.assertFalse(item.is_read)
        item.mark_read()
        self.assertTrue(Notification.objects.get(pk=item.pk).is_read)
