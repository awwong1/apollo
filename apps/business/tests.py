from apps.business.models import Business, BusinessMembership, LastAdministratorException
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


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
        membership.delete()
        self.assertIsNone(membership.pk)
        self.assertIsNone(business.pk)
        business = Business.objects.create(
            name="X",
            description="Testing business known as X.",
            address_1="345 Test Drive",
            address_2="789 Boulevard Test",
            postal_code="T3S7E4",
        )
        user2 = User.objects.create_user('testUser2', 'test2@example.com', 'password')
        membership = BusinessMembership.objects.create(user=user, business=business, business_administrator=True)
        BusinessMembership.objects.create(user=user2, business=business, business_administrator=True)
        membership.delete()
        self.assertIsNone(membership.pk)
        self.assertIsNotNone(business.pk)

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
        self.assertRaises(LastAdministratorException, membership.clean)
        user2 = User.objects.create_user('testUser2', 'test2@example.com', 'password')
        BusinessMembership.objects.create(user=user2, business=business, business_administrator=True)
        membership.business_administrator = False
        membership.save()

    def test_readonly_fields_after_add(self):
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
        membership.user = user2  # This instance of business membership has invalid user
        self.assertEqual(membership.user, user2)
        membership.clean()  # This instance of business has valid membership user again
        self.assertEqual(membership.user, user)
        membership = BusinessMembership.objects.all()[0]
        self.assertEqual(membership.user, user)
        business2 = Business.objects.create(
            name="Y",
            description="Testing business known as Y.",
            address_1="PLM Test Drive",
            address_2="OKN Boulevard Test",
            postal_code="T3S7E4",
        )
        membership.business = business2
        membership.clean()
        self.assertEqual(membership.business, business)


class BusinessAPITestCase(APITestCase):
    def setUp(self):
        User.objects.create_user('test', 'test@example.com', 'password')

    def test_business_post(self):
        """
        Test for business object creation with our API
        """
        url = reverse('business-list')
        data = {
            "city": None,
            "name": u"Business API Test",
            "description": u"This is a test business for API adding.",
            "address_1": u"Test Drive 123 Way",
            "address_2": u"Mark Boulevard 345",
            "postal_code": u"Z0Z0Z0"
        }

        # Must be logged in to create businesses
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.login(username='test', password='password')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['city'], data['city'])
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['description'], data['description'])
        self.assertEqual(response.data['address_1'], data['address_1'])
        self.assertEqual(response.data['address_2'], data['address_2'])
        self.assertEqual(response.data['postal_code'], data['postal_code'])
        self.assertIsNotNone(response.data['url'])
        # Auto created business membership
        business_membership = BusinessMembership.objects.all()[0]
        business = Business.objects.all()[0]
        self.assertEqual(business_membership.business.pk, business.pk)

    def test_business_put(self):
        """
        Test to ensure full object updates function properly
        """
        data = {
            "city": None,
            "name": u"Business API Test",
            "description": u"This is a test business for API adding.",
            "address_1": u"Test Drive 123 Way",
            "address_2": u"Mark Boulevard 345",
            "postal_code": u"Z0Z0Z0"
        }
        business = Business.objects.create(
            city=data['city'],
            name=data['name'],
            description=data['description'],
            address_1=data['address_1'],
            address_2=data['address_2'],
            postal_code=data['postal_code']
        )
        url = reverse('business-detail', kwargs={'pk': business.pk})

        user = User.objects.get(username='test')

        # Not authenticated, throw 403 forbidden
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Not a member of the business, throw 403 forbidden
        self.client.login(username='test', password='password')
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Membership is not administrator, throw 403 forbidden
        business_membership = BusinessMembership.objects.create(
            user=user,
            business=business
        )
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Membership is an administrator for business, allow put
        business_membership.business_administrator = True
        business_membership.save()
        data['name'] = "Modified Business Name"
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], data['name'])

    def test_business_patch(self):
        """
        Test to ensure partial updates function properly
        """
        data = {
            "city": None,
            "name": u"Business API Test",
            "description": u"This is a test business for API adding.",
            "address_1": u"Test Drive 123 Way",
            "address_2": u"Mark Boulevard 345",
            "postal_code": u"Z0Z0Z0"
        }
        business = Business.objects.create(
            city=data['city'],
            name=data['name'],
            description=data['description'],
            address_1=data['address_1'],
            address_2=data['address_2'],
            postal_code=data['postal_code']
        )
        url = reverse('business-detail', kwargs={'pk': business.pk})

        user = User.objects.get(username='test')

        # Not authenticated, throw 403 forbidden
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Not a member of the business, throw 403 forbidden
        self.client.login(username='test', password='password')
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Membership is not administrator, throw 403 forbidden
        business_membership = BusinessMembership.objects.create(
            user=user,
            business=business
        )
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Membership is an administrator for business, allow put
        business_membership.business_administrator = True
        business_membership.save()
        patch_data = {"name": "Modified Business Name"}
        response = self.client.patch(url, patch_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], patch_data['name'])

    def test_business_delete(self):
        """
        Test to ensure businesses may not be deleted with our API
        """
        data = {
            "city": None,
            "name": u"Business API Test",
            "description": u"This is a test business for API adding.",
            "address_1": u"Test Drive 123 Way",
            "address_2": u"Mark Boulevard 345",
            "postal_code": u"Z0Z0Z0"
        }
        business = Business.objects.create(
            city=data['city'],
            name=data['name'],
            description=data['description'],
            address_1=data['address_1'],
            address_2=data['address_2'],
            postal_code=data['postal_code']
        )
        url = reverse('business-detail', kwargs={'pk': business.pk})
        user = User.objects.get(username='test')

        # Not logged in, forbidden
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Not a member of the business, throw 403 forbidden
        self.client.login(username='test', password='password')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Membership is not administrator, throw 403 forbidden
        business_membership = BusinessMembership.objects.create(
            user=user,
            business=business
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Membership is an administrator for business, delete is forbidden
        business_membership.business_administrator = True
        business_membership.save()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
