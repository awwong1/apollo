from apps.equipment.models import Equipment, Service
from django.contrib.auth.models import User
from django.test import TestCase


class EquipmentServiceTestCase(TestCase):
    def test_user_permissions(self):
        user = User.objects.create_user('testUser', 'test@example.com', 'password')
        super_user = User.objects.create_superuser('admin', 'admin@example.com', 'password')

        self.assertFalse(user.has_perm('equipment.add_equipment'))
        self.assertFalse(user.has_perm('equipment.change_equipment'))
        self.assertFalse(user.has_perm('equipment.delete_equipment'))
        self.assertTrue(super_user.has_perm('equipment.add_equipment'))
        self.assertTrue(super_user.has_perm('equipment.change_equipment'))
        self.assertTrue(super_user.has_perm('equipment.delete_equipment'))

        self.assertFalse(user.has_perm('equipment.add_service'))
        self.assertFalse(user.has_perm('equipment.change_service'))
        self.assertFalse(user.has_perm('equipment.delete_service'))
        self.assertTrue(super_user.has_perm('equipment.add_service'))
        self.assertTrue(super_user.has_perm('equipment.change_service'))
        self.assertTrue(super_user.has_perm('equipment.delete_service'))

    def test_creation(self):
        equipment = Equipment.objects.create(
            name="Fancy Laser",
            description="This is a fancy laser cannon"
        )
        self.assertEqual(equipment, Equipment.objects.get(pk=equipment.pk))
        service = Service.objects.create(
            name="Fancy Laser Service",
            activation_id="LASER-(.*)",
            activate=equipment,
        )
        self.assertEqual(service.activate, Equipment.objects.get(pk=service.pk))
        self.assertEqual(equipment.service_set.all()[0], service)

    def test_activation(self):
        equipment = Equipment.objects.create(
            name="Fancy Laser",
            description="This is a fancy laser cannon"
        )
        service = Service.objects.create(
            name="Fancy Laser Service",
            activation_id="^LASER-(.*)",
            activate=equipment,
        )
        self.assertFalse(service.activates("DRILL-1234"))
        self.assertFalse(service.activates("NOT_A_LASER-1234"))
        self.assertTrue(service.activates("LASER-1234"))
