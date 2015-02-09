from apollo.choices import PRICE_LIST_RELEASE
from apps.price_list.models import PriceList, ActivityPriceListItem, TimePriceListItem, UnitPriceListItem, PriceListBundle
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
        bundle = PriceListBundle.objects.create(
            price_list=price_list,
            percent_discount=50
        )
        bundle.activity_bundle_items.add(activity_item)
        bundle.time_bundle_items.add(time_item)
        bundle.unit_bundle_items.add(unit_item)
        self.assertEqual(price_list.activitypricelistitem_set.all()[0], activity_item)
        self.assertEqual(price_list.timepricelistitem_set.all()[0], time_item)
        self.assertEqual(price_list.unitpricelistitem_set.all()[0], unit_item)
        self.assertEqual(price_list.pricelistbundle_set.all()[0], bundle)

        price_list.status = PRICE_LIST_RELEASE
        price_list.save()

        price_list.name = "Attempt to change"
        self.assertRaises(ValidationError, price_list.clean)
        self.assertRaises(ValidationError, activity_item.clean)
        self.assertRaises(ValidationError, time_item.clean)
        self.assertRaises(ValidationError, unit_item.clean)

        next_price_list = price_list.create_next_price_list(name="Next Test Price List", description="Price List Deux")
        self.assertEqual(next_price_list.activitypricelistitem_set.all()[0].item_uuid,
                         "00000000-0000-0000-0000-000000000000")
        self.assertEqual(next_price_list.timepricelistitem_set.all()[0].item_uuid,
                         "10000000-0000-0000-0000-000000000000")
        self.assertEqual(next_price_list.unitpricelistitem_set.all()[0].item_uuid,
                         "20000000-0000-0000-0000-000000000000")
        self.assertNotEqual(price_list, next_price_list)

        self.assertNotEqual(next_price_list.pricelistbundle_set.all()[0], bundle)
        self.assertEqual(next_price_list.pricelistbundle_set.all()[0].activity_bundle_items.all()[0].item_uuid,
                         "00000000-0000-0000-0000-000000000000")
        self.assertEqual(next_price_list.pricelistbundle_set.all()[0].time_bundle_items.all()[0].item_uuid,
                         "10000000-0000-0000-0000-000000000000")
        self.assertEqual(next_price_list.pricelistbundle_set.all()[0].unit_bundle_items.all()[0].item_uuid,
                         "20000000-0000-0000-0000-000000000000")

    def test_bundle_cost_calculation(self):
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
        bundle = PriceListBundle(
            price_list=price_list,
            percent_discount=-1
        )
        self.assertRaises(ValidationError, bundle.clean)
        bundle.percent_discount = 200
        self.assertRaises(ValidationError, bundle.clean)

        bundle.percent_discount = 50
        bundle.save()

        bundle.activity_bundle_items.add(activity_item)
        bundle.time_bundle_items.add(time_item)
        bundle.unit_bundle_items.add(unit_item)
        activity_item_cost = bundle.get_bundle_items_cost(item_classes=[ActivityPriceListItem])
        self.assertEqual(activity_item_cost[activity_item], (5.0, 'Test'))
        time_item_cost = bundle.get_bundle_items_cost(item_classes=[TimePriceListItem])
        self.assertEqual(time_item_cost[time_item], (5.0, 60))
        unit_item_cost = bundle.get_bundle_items_cost(item_classes=[UnitPriceListItem])
        self.assertEqual(unit_item_cost[unit_item], 5.0)
