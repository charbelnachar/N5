import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'app.settings.base'
import django

django.setup()
from app.src.vehicle.vehicle_logic import VehicleLogic
import unittest
from unittest.mock import patch, MagicMock
from app.models import Vehicle, Person
from app.src.serializer.serializers import VehicleSerializer
from app.src.exception.custom_exep import InvalidIdentifierError, InvalidDataError


class TestVehicleLogic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.vehicle_logic = VehicleLogic()

    def setUp(self):
        self.owner = Person.objects.create(name='Alice Smith', email='alice.smith@example.com')
        self.vehicle = Vehicle.objects.create(license_plate='ABC123', brand='Toyota', color='Red', owner=self.owner)

        self.owner_2 = Person.objects.create(name='Bob Johnson', email='bob.johnson@example.com')
        self.vehicle_2 = Vehicle.objects.create(license_plate='XYZ789', brand='Honda', color='Blue', owner=self.owner_2)

        self.mock_vehicle_data = {
            'license_plate': 'ABC123',
            'brand': 'Toyota',
            'color': 'Red',
            'owner': self.owner.id
        }
        self.mock_vehicle_data_2 = {
            'license_plate': 'XYZ789',
            'brand': 'Honda',
            'color': 'Blue',
            'owner': self.owner_2.id
        }

    def tearDown(self):
        self.vehicle.delete()
        self.owner.delete()
        self.vehicle_2.delete()
        self.owner_2.delete()

    @patch('app.src.serializer.serializers.VehicleSerializer')
    def test_get_vehicle(self, mock_serializer):
        mock_serializer.return_value.data = {
            'license_plate': 'ABC123',
            'brand': 'Toyota',
            'color': 'Red',
            'owner': self.owner.id
        }

        result = self.vehicle_logic.get_vehicle('ABC123')
        self.assertEqual(result['license_plate'], mock_serializer.return_value.data['license_plate'])

        with self.assertRaises(InvalidIdentifierError):
            self.vehicle_logic.get_vehicle('nonexistent')

    @patch('app.src.serializer.serializers.VehicleSerializer')
    def test_get_all_vehicles(self, mock_serializer):
        result = self.vehicle_logic.get_all_vehicles()
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)

    @patch('app.src.serializer.serializers.VehicleSerializer')
    def test_modify_vehicle(self, mock_serializer):
        mock_serializer.return_value.is_valid.return_value = True
        mock_serializer.return_value.data = {
            'license_plate': 'ABC123',
            'brand': 'Toyota',
            'color': 'Blue',
            'owner': self.owner.id
        }

        updated_data = {'license_plate': 'ABC123', 'brand': 'Toyota', 'color': 'Blue', 'owner': self.owner.id}
        result = self.vehicle_logic.modify_vehicle('ABC123', updated_data)
        self.assertEqual(result['color'], mock_serializer.return_value.data['color'])

        with self.assertRaises(InvalidDataError):
            self.vehicle_logic.modify_vehicle('nonexistent', updated_data)

    @patch('app.src.serializer.serializers.VehicleSerializer')
    def test_delete_vehicle(self, mock_serializer):
        self.vehicle_logic.delete_vehicle('ABC123')
        with self.assertRaises(Vehicle.DoesNotExist):
            Vehicle.objects.get(license_plate='ABC123')

        with self.assertRaises(InvalidIdentifierError):
            self.vehicle_logic.delete_vehicle('nonexistent')

    @patch('app.src.serializer.serializers.VehicleSerializer')
    def test_create_vehicle(self, mock_serializer):
        mock_serializer.return_value.is_valid.return_value = True

        new_vehicle_data = {
            'license_plate': 'NEW123',
            'brand': 'Ford',
            'color': 'Green',
            'owner': self.owner.id
        }

        result = self.vehicle_logic.create_vehicle(new_vehicle_data)
        self.assertEqual(result['license_plate'], new_vehicle_data['license_plate'])
        vehicle = Vehicle.objects.get(license_plate=new_vehicle_data['license_plate'])
        vehicle.delete()

        with self.assertRaises(InvalidDataError):
            self.vehicle_logic.create_vehicle({'license_plate': 'ABC123'})


if __name__ == '__main__':
    unittest.main()
