import re
from apps.business.models import Business, BusinessMembership
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class BusinessAPITestCase(APITestCase):
    user = None
    superuser = None
    business = None
    su_business_membership = None

    def setUp(self):
        self.user = User.objects.create_user('test', 'test@example.com', 'password')
        self.superuser = User.objects.create_user('supertest', 'supertest@example.com', 'password')
        self.business = Business.objects.create(name="X", description="Testing business known as X.",
                                                address_1="345 Test Drive", address_2="789 Boulevard Test",
                                                postal_code="T3S7E4", )
        self.su_business_membership = BusinessMembership.objects.create(user=self.superuser, business=self.business,
                                                                        business_administrator=True)

    def test_business_user_permissions(self):
        """
        Test for if the permissions defined for a business instance are valid per user.
        :return:
        """
        # All users can create a business.
        self.assertTrue(self.user.has_perm('business.add_business'))
        self.assertFalse(self.user.has_perm('business.change_business'))
        self.assertFalse(self.user.has_perm('business.add_businessmembership'))
        self.assertFalse(self.user.has_perm('business.change_businessmembership'))
        self.assertFalse(self.user.has_perm('business.delete_businessmembership'))

        # but they cannot modify businesses they are not administrators of.
        self.assertFalse(self.user.has_perm('business.change_business', self.business))
        self.assertFalse(self.user.has_perm('business.add_businessmembership', self.business))
        self.assertFalse(self.user.has_perm('business.change_businessmembership'))
        self.assertFalse(self.user.has_perm('business.delete_businessmembership'))

        # Non business administrator users do not gain any business instance permissions.
        memb = BusinessMembership.objects.create(user=self.user, business=self.business, business_administrator=False)
        self.assertFalse(self.user.has_perm('business.change_business', self.business))
        self.assertFalse(self.user.has_perm('business.add_businessmembership', self.business))
        self.assertFalse(self.user.has_perm('business.change_businessmembership'))
        self.assertFalse(self.user.has_perm('business.delete_businessmembership'))

        # Business administrator users can edit and delete their own business, but not others.
        memb.business_administrator = True
        memb.save()
        self.assertTrue(self.user.has_perm('business.change_business', self.business))
        self.assertTrue(self.user.has_perm('business.add_businessmembership', self.business))
        self.assertTrue(self.user.has_perm('business.change_businessmembership', self.business))
        self.assertTrue(self.user.has_perm('business.delete_businessmembership', self.business))
        new_business = Business.objects.create(name="Y", description="Testing business known as Y.",
                                               address_1="ABC Test Drive", address_2="DEF Boulevard Test",
                                               postal_code="T3S7E4", )
        self.assertFalse(self.user.has_perm('business.change_business', new_business))
        self.assertFalse(self.user.has_perm('business.add_businessmembership', new_business))
        self.assertFalse(self.user.has_perm('business.change_businessmembership'))
        self.assertFalse(self.user.has_perm('business.delete_businessmembership'))

    def test_api_business_post_invalid(self):
        """
        Test for if creating a business with the api handles invalid/missing data
        :return:
        """
        url = reverse('business-list')
        data = {"name": u"Business API Test"}

        # Unauthenticated users will not be able to create a business
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Authenticated users will be able to create a business, but data is invalid
        self.client.login(username='test', password='password')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_business_post_valid(self):
        """
        Test for if creating a business with the api is handled properly and triggers valid action hooks
        :return:
        """
        url = reverse('business-list')
        data = {"city": None, "name": u"Business API Test", "description": u"This is a test business for API adding.",
                "address_1": u"Test Drive 123 Way", "address_2": u"Mark Boulevard 345", "postal_code": u"Z0Z0Z0"}

        # Unauthenticated users will not be able to create a business
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Authenticated users will be able to create a business
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
        b_id = re.search("([\d]*)/$", response.data['url']).group(1)

        # Creating a business using django rest automatically creates a business administrator business membership
        business_membership = BusinessMembership.objects.filter(business__pk=b_id)[0]
        business = Business.objects.get(pk=b_id)
        self.assertEqual(business_membership.business.pk, business.pk)
        self.assertEqual(business_membership.user, self.user)

    def test_api_business_membership_post_invalid(self):
        """
        Test for if creating a business membership with the api handles invalid data
        :return:
        """
        url = reverse('business-membership-list')
        business_invalid_url = self.business.pk
        user_invalid_url = self.user.pk
        data = {"business": business_invalid_url, "user": user_invalid_url, "business_administrator": False}

        # Cannot create a business membership if you are not authenticated
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Cannot create a business membership for a business that you are not a business administrator of
        self.assertFalse(self.user.has_perm("business.add_businessmembership", self.business))
        self.client.login(username='test', password='password')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_FORBIDDEN)

        # Only the business administrator can create memberships for their business, but data is invalid
        self.client.login(username='supertest', password='password')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_business_membership_post_valid(self):
        """
        Test for if creating a business membership with the api is handled properly
        :return:
        """
        url = reverse('business-membership-list')
        b_instance_raw_response = self.client.get('/api/business/business/{pk}/'.format(pk=self.business.pk),
                                                  format='json')
        business_instance_url = b_instance_raw_response.data["url"]
        user_instance_raw_response = self.client.get('/api/account/user/{pk}/'.format(pk=self.user.pk), format='json')
        user_instance_url = user_instance_raw_response.data["url"]
        data = {"business": business_instance_url, "user": user_instance_url, "business_administrator": False}

        # Cannot create a business membership if you are not authenticated
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Cannot create a business membership for a business that you are not a business administrator of
        self.assertFalse(self.user.has_perm("business.add_businessmembership", self.business))
        self.client.login(username='test', password='password')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Only the business administrator can create memberships for their business
        self.client.login(username='supertest', password='password')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

