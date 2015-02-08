from uuid import uuid4
from apollo.choices import PRICE_LIST_RELEASE
from apps.price_list.models import PriceList, ActivityPriceListItem, TimePriceListItem, UnitPriceListItem
from apps.terms_of_service.models import TermsOfService
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase


class PriceListTestCase(TestCase):
    def setUp(self):
        TermsOfService.objects.create(
            title="Test Terms of Service",
            content="Terms and Conditions that no one reads anyways~"
        )

    def test_user_permissions(self):
        user = User.objects.create_user('testUser', 'test@example.com', 'password')
        super_user = User.objects.create_superuser('admin', 'admin@example.com', 'password')

        self.assertFalse(user.has_perm('price_list.add_pricelist'))
        self.assertFalse(user.has_perm('price_list.change_pricelist'))
        self.assertFalse(user.has_perm('price_list.delete_pricelist'))
        self.assertTrue(super_user.has_perm('price_list.add_pricelist'))
        self.assertTrue(super_user.has_perm('price_list.change_pricelist'))
        self.assertTrue(super_user.has_perm('price_list.delete_pricelist'))

    def test_creation(self):
        price_list = PriceList.objects.create(
            name="Test Price List",
            description="Price list for testing purposes"
        )
        activity_item = ActivityPriceListItem.objects.create(
            price_list=price_list,
            item_uuid="00000000-0000-0000-0000-000000000000",
            name="Test Activity Item",
            description="This is a test activity item for testing purposes only.",
            terms_of_service=TermsOfService.objects.get(pk=1),
            price_per_unit=10.0,
            unit_measurement='Test'
        )
        time_item = TimePriceListItem.objects.create(
            price_list=price_list,
            item_uuid="10000000-0000-0000-0000-000000000000",
            name="Test Time Item",
            description="This is a test time item for testing purposes only.",
            terms_of_service=TermsOfService.objects.get(pk=1),
            price_per_time=10.0,
            unit_time=60
        )
        unit_item = UnitPriceListItem.objects.create(
            price_list=price_list,
            item_uuid="20000000-0000-0000-0000-000000000000",
            name="Test Unit Item",
            description="This is a test unit item for testing purposes only.",
            terms_of_service=TermsOfService.objects.get(pk=1),
            price_per_unit=10.0,
        )
        self.assertEqual(price_list.activitypricelistitem_set.all()[0], activity_item)
        self.assertEqual(price_list.timepricelistitem_set.all()[0], time_item)
        self.assertEqual(price_list.unitpricelistitem_set.all()[0], unit_item)

        price_list.status = PRICE_LIST_RELEASE
        price_list.save()

        price_list.name = "Attempt to change"
        self.assertRaises(ValidationError, price_list.save)
        self.assertRaises(ValidationError, activity_item.save)
        self.assertRaises(ValidationError, time_item.save)
        self.assertRaises(ValidationError, unit_item.save)

        next_price_list = price_list.create_next_price_list(name="Next Test Price List", description="Price List Deux")
        self.assertEqual(next_price_list.activitypricelistitem_set.all()[0].item_uuid,
                         "00000000-0000-0000-0000-000000000000")
        self.assertEqual(next_price_list.timepricelistitem_set.all()[0].item_uuid,
                         "10000000-0000-0000-0000-000000000000")
        self.assertEqual(next_price_list.unitpricelistitem_set.all()[0].item_uuid,
                         "20000000-0000-0000-0000-000000000000")
        self.assertNotEqual(price_list, next_price_list)