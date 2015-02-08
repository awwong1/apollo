from apps.terms_of_service.models import TermsOfService
from django.contrib.auth.models import User
from django.test import TestCase
from time import time, mktime, sleep


class TermsOfServiceTestCase(TestCase):
    def test_user_permissions(self):
        user = User.objects.create_user('testUser', 'test@example.com', 'password')
        super_user = User.objects.create_superuser('admin', 'admin@example.com', 'password')

        self.assertFalse(user.has_perm('terms_of_service.add_termsofservice'))
        self.assertFalse(user.has_perm('terms_of_service.change_termsofservice'))
        self.assertFalse(user.has_perm('terms_of_service.delete_termsofservice'))
        self.assertTrue(super_user.has_perm('terms_of_service.add_termsofservice'))
        self.assertTrue(super_user.has_perm('terms_of_service.change_termsofservice'))
        self.assertTrue(super_user.has_perm('terms_of_service.delete_termsofservice'))

    def test_creation(self):
        time_start = time()
        sleep(1)
        tos = TermsOfService.objects.create(
            title="Test Terms of Service",
            content="Terms and conditions that no body ever bothers to read anyways"
        )
        sleep(1)
        time_end = time()
        self.assertIsNotNone(tos.pk)
        tos_epoch_creation = mktime(tos.date_created.timetuple())
        self.assertLessEqual(tos_epoch_creation, time_end)
        self.assertGreaterEqual(tos_epoch_creation, time_start)
