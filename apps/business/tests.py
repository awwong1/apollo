from apps.business.models import Business
from cities_light.models import Country, Region, City
from django.contrib.auth.models import User, Permission
from django.test import TestCase


class BusinessTestCase(TestCase):

    def test_user_business_permissions(self):
        user = User(username="test")
        user.save()

        business = Business(
            name="X",
            description="Testing business known as X.",
            address_1="345 Test Drive",
            address_2="789 Boulevard Test",
            postal_code="T3S7E4"
        )
        business.save()
