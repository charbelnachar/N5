import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'app.settings.base'
import django

django.setup()
from app.src.violation.violation_logic import ViolationLogic
import unittest
from unittest.mock import patch, MagicMock
from django.contrib.auth.models import User
from app.models import Person, Violation, Vehicle, Officer
from app.src.exception.custom_exep import InvalidDataError, InvalidIdentifierError


class TestViolationLogic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.violation_logic = ViolationLogic()

    def setUp(self):
        self.owner = Person.objects.create(name='Unique Alice', email='unique.alice@example.com')
        self.owner_2 = Person.objects.create(name='Unique Bob', email='unique.bob@example.com')

        self.vehicle = Vehicle.objects.create(license_plate='UNQ123', brand='Toyota', color='Red', owner=self.owner)
        self.vehicle_2 = Vehicle.objects.create(license_plate='UNQ456', brand='Honda', color='Blue', owner=self.owner_2)

        self.user = User.objects.create_user(username='officeruser', password='password123', email='officer@example.com')
        self.officer = Officer.objects.create(user=self.user, name='Officer One', identifier='OFF123')

        self.violation = Violation.objects.create(vehicle=self.vehicle, timestamp='2023-01-01T00:00:00Z', comments='Speeding', officer=self.officer)
        self.violation_2 = Violation.objects.create(vehicle=self.vehicle_2, timestamp='2023-01-02T00:00:00Z', comments='Parking', officer=self.officer)

        self.mock_violation_data = {
            'license_plate': 'UNQ123',
            'timestamp': '2023-01-01T00:00:00Z',
            'comments': 'Speeding',
            'officer': self.officer.id
        }
        self.mock_violation_data_2 = {
            'license_plate': 'UNQ456',
            'timestamp': '2023-01-02T00:00:00Z',
            'comments': 'Parking',
            'officer': self.officer.id
        }

    def tearDown(self):
        self.violation.delete()
        self.violation_2.delete()
        self.vehicle.delete()
        self.vehicle_2.delete()
        self.owner.delete()
        self.owner_2.delete()
        self.officer.delete()
        self.user.delete()

    @patch('app.src.serializer.serializers.ViolationSerializer')
    def test_get_violations_by_email(self, mock_serializer):
        mock_serializer.return_value.data = [self.mock_violation_data, self.mock_violation_data_2]

        result = self.violation_logic.get_violations_by_email('unique.alice@example.com')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['comments'], self.mock_violation_data['comments'])

        with self.assertRaises(InvalidDataError):
            self.violation_logic.get_violations_by_email('invalidemail')

    @patch('app.src.serializer.serializers.ViolationSerializer')
    def test_create_violation(self, mock_serializer):
        mock_serializer.return_value.is_valid.return_value = True
        mock_serializer.return_value.data = self.mock_violation_data

        new_violation_data = {
            'license_plate': 'UNQ123',
            'timestamp': '2023-01-03T00:00:00Z',
            'comments': 'Illegal Turn',
            'officer': self.officer.id
        }

        result = self.violation_logic.create_violation(new_violation_data, self.officer)
        self.assertEqual(result['comments'], new_violation_data['comments'])
        violation = Violation.objects.get(vehicle=self.vehicle, comments='Illegal Turn')
        violation.delete()

    @patch('app.src.serializer.serializers.ViolationSerializer')
    def test_get_violation(self, mock_serializer):
        mock_serializer.return_value.data = self.mock_violation_data

        result = self.violation_logic.get_violation(self.violation.id)
        self.assertEqual(result['comments'], self.mock_violation_data['comments'])

        with self.assertRaises(InvalidIdentifierError):
            self.violation_logic.get_violation(999)

    @patch('app.src.serializer.serializers.ViolationSerializer')
    def test_get_all_violations(self, mock_serializer):
        result = self.violation_logic.get_all_violations()
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)

    @patch('app.src.serializer.serializers.ViolationSerializer')
    def test_update_violation(self, mock_serializer):
        mock_serializer.return_value.is_valid.return_value = True
        mock_serializer.return_value.data = {
            'license_plate': 'UNQ123',
            'timestamp': '2023-01-01T00:00:00Z',
            'comments': 'Updated Comment',
            'officer': self.officer.id
        }

        updated_data = {'comments': 'Updated Comment'}
        result = self.violation_logic.update_violation(self.violation.id, updated_data)
        self.assertEqual(result['comments'], 'Updated Comment')

        with self.assertRaises(InvalidIdentifierError):
            self.violation_logic.update_violation(999, updated_data)

    def test_delete_violation(self):
        self.violation_logic.delete_violation(self.violation.id)
        with self.assertRaises(Violation.DoesNotExist):
            Violation.objects.get(id=self.violation.id)

        with self.assertRaises(InvalidIdentifierError):
            self.violation_logic.delete_violation(999)


if __name__ == '__main__':
    unittest.main()
