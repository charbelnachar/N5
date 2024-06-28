import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'app.settings.base'
import django

django.setup()
from app.src.officer.officer_logic import OfficerLogic
import unittest
from unittest.mock import patch, MagicMock
from django.contrib.auth.models import User

from app.models import Officer
from app.src.serializer.serializers import OfficerSerializer
from app.src.exception.custom_exep import InvalidIdentifierError, InvalidDataError

class TestOfficerLogic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.officer_logic = OfficerLogic()
        cls.mock_officer_data = {
            'username': 'uniqueuser12',
            'name': 'Alice Smith',
            'email': '2alice.smith@example.com',
            'identifier': 'ABC123',
            'password': 'alicepassword'
        }
        cls.mock_officer_data_2 = {
            'username': 'uniqueuser22',
            'name': 'Bob Johnson',
            'email': '2bob.johnson@example.com',
            'identifier': 'XYZ7892',
            'password': 'bobpassword'
        }

    def setUp(self):
        self.user = User.objects.create_user(username='uniqueuser12', password='alicepassword', email='2alice.smith@example.com')
        self.officer = Officer.objects.create(user=self.user, name='Alice Smith', identifier='ABC123')

        self.user_2 = User.objects.create_user(username='uniqueuser22', password='bobpassword', email='2bob.johnson@example.com')
        self.officer_2 = Officer.objects.create(user=self.user_2, name='Bob Johnson', identifier='XYZ7892')

    def tearDown(self):
        self.officer.delete()
        self.user.delete()
        self.officer_2.delete()
        self.user_2.delete()

    @patch('app.src.serializer.serializers.OfficerSerializer')
    def test_get_officer(self, mock_serializer):
        mock_serializer.return_value.data = {
            'username': 'uniqueuser1',
            'name': 'Alice Smith',
            'email': 'alice.smith@example.com',
            'identifier': 'ABC123'
        }

        result = self.officer_logic.get_officer('ABC123')
        self.assertEqual(result['identifier'], mock_serializer.return_value.data['identifier'])

        with self.assertRaises(InvalidIdentifierError):
            self.officer_logic.get_officer('nonexistent')

    @patch('app.src.serializer.serializers.OfficerSerializer')
    def test_get_all_officers(self, mock_serializer):


        result = self.officer_logic.get_all_officers()
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)


    @patch('app.src.serializer.serializers.OfficerSerializer')
    def test_modify_officer(self, mock_serializer):
        mock_serializer.return_value.is_valid.return_value = True
        mock_serializer.return_value.data = {
            'username': 'uniqueuser1',
            'name': 'Alice Johnson',
            'email': 'alice.johnson@example.com',
            'identifier': 'ABC123'
        }

        updated_data = {'name': 'Alice Johnson', 'identifier': 'ABC123', 'email': 'alice.johnson@example.com', 'username': 'alicejohnson'}
        result = self.officer_logic.modify_officer('ABC123', updated_data)
        self.assertEqual(result['email'], mock_serializer.return_value.data['email'])

        with self.assertRaises(ValueError):
            self.officer_logic.modify_officer('nonexistent', updated_data)

    @patch('app.src.serializer.serializers.OfficerSerializer')
    def test_delete_officer(self, mock_serializer):
        self.officer_logic.delete_officer('ABC123')
        with self.assertRaises(Officer.DoesNotExist):
            Officer.objects.get(identifier='ABC123')

        with self.assertRaises(InvalidIdentifierError):
            self.officer_logic.delete_officer('nonexistent')

    @patch('app.src.serializer.serializers.OfficerSerializer')
    def test_create_officer(self, mock_serializer):
        mock_serializer.return_value.is_valid.return_value = True

        new_officer_data = {
            'username': 'newauniqueusaer',
            'name': 'Charliea Barown',
            'email': 'chaaralie.brown@example.com',
            'password': 'chaarliaepassword',
            'identifier': 'LaMN456a'
        }

        result = self.officer_logic.create_officer(new_officer_data)
        self.assertEqual(result['identifier'], new_officer_data['identifier'])
        officer = Officer.objects.get(identifier=new_officer_data['identifier'])
        user = officer.user
        officer.delete()
        user.delete()

        with self.assertRaises(InvalidDataError):
            self.officer_logic.create_officer({'username': ''})


if __name__ == '__main__':
    unittest.main()