from apps.business.models import Business, BusinessMembership, LastAdministratorException
from django.contrib.auth.models import User
from django.test import TestCase


class BusinessTestCase(TestCase):
    def test_user_add_businesses_permission(self):
        user = User.objects.create_user('testUser', 'test@example.com', 'password')
        self.assertTrue(user.has_perm('business.add_business'))

    def test_user_business_ownership_permission(self):
        user = User.objects.create_user('testUser', 'test@example.com', 'password')
        business = Business.objects.create(
            name="X",
            description="Testing business known as X.",
            address_1="345 Test Drive",
            address_2="789 Boulevard Test",
            postal_code="T3S7E4",
        )
        self.assertFalse(user.has_perm('business.change_business', business))
        self.assertFalse(user.has_perm('business.add_businessmembership', business))

        membership = BusinessMembership.objects.create(user=user, business=business, business_administrator=True)

        self.assertTrue(user.has_perm('business.change_business', business))
        self.assertTrue(user.has_perm('business.add_businessmembership', business))
        self.assertTrue(user.has_perm('business.change_businessmembership', membership))
        self.assertTrue(user.has_perm('business.delete_businessmembership', membership))

        user2 = User.objects.create_user('testUser2', 'test2@example.com', 'password')
        BusinessMembership.objects.create(user=user2, business=business, business_administrator=True)
        membership.business_administrator = False
        membership.save()

        self.assertFalse(user.has_perm('business.change_business', business))
        self.assertFalse(user.has_perm('business.add_businessmembership', business))
        self.assertFalse(user.has_perm('business.change_businessmembership', membership))
        self.assertFalse(user.has_perm('business.delete_businessmembership', membership))

    def test_delete_last_business_admin(self):
        user = User.objects.create_user('testUser', 'test@example.com', 'password')
        business = Business.objects.create(
            name="X",
            description="Testing business known as X.",
            address_1="345 Test Drive",
            address_2="789 Boulevard Test",
            postal_code="T3S7E4",
        )
        membership = BusinessMembership.objects.create(user=user, business=business, business_administrator=True)
        self.assertRaises(LastAdministratorException, membership.delete)
        user2 = User.objects.create_user('testUser2', 'test2@example.com', 'password')
        BusinessMembership.objects.create(user=user2, business=business, business_administrator=True)
        membership.delete()

    def test_modify_last_business_admin(self):
        user = User.objects.create_user('testUser', 'test@example.com', 'password')
        business = Business.objects.create(
            name="X",
            description="Testing business known as X.",
            address_1="345 Test Drive",
            address_2="789 Boulevard Test",
            postal_code="T3S7E4",
        )
        membership = BusinessMembership.objects.create(user=user, business=business, business_administrator=True)
        membership.business_administrator = False
        self.assertRaises(LastAdministratorException, membership.save)
        user2 = User.objects.create_user('testUser2', 'test2@example.com', 'password')
        BusinessMembership.objects.create(user=user2, business=business, business_administrator=True)
        membership.business_administrator = False
        membership.save()

    def test_readonly_after_add(self):
        user = User.objects.create_user('testUser', 'test@example.com', 'password')
        business = Business.objects.create(
            name="X",
            description="Testing business known as X.",
            address_1="345 Test Drive",
            address_2="789 Boulevard Test",
            postal_code="T3S7E4",
        )
        membership = BusinessMembership(user=user, business=business, business_administrator=True)
        self.assertEqual(None, membership.pk)
        membership.save()
        self.assertNotEqual(None, membership.pk)
        user2 = User.objects.create_user('testUser2', 'test2@example.com', 'password')
        membership.user = user2  # This instance of business membership is invalid
        self.assertEqual(membership.user, user2)
        membership.save()  # This instance of business membership is valid again
        self.assertEqual(membership.user, user)
        membership = BusinessMembership.objects.all()[0]
        self.assertEqual(membership.user, user)