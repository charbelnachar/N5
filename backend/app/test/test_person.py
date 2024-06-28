import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'app.settings.base'
import django

django.setup()
from app.src.person.person_logic import PersonLogic
import unittest
from unittest.mock import patch, MagicMock
from app.models import Person
from app.src.serializer.serializers import PersonSerializer
from app.src.exception.custom_exep import InvalidIdentifierError, InvalidDataError
from app.src.utility.util_data import UtilData
from app.src.utility.util_email import EmailValidator


class TestPersonLogic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.person_logic = PersonLogic()
        cls.mock_person_data = {
            'name': 'Alice Smith',
            'email': 'alice.smith@example.com'
        }
        cls.mock_person_data_2 = {
            'name': 'Bob Johnson',
            'email': 'bob.johnson@example.com'
        }

    def setUp(self):
        self.person = Person.objects.create(name='Alice Smith', email='alice.smith@example.com')
        self.person_2 = Person.objects.create(name='Bob Johnson', email='bob.johnson@example.com')

    def tearDown(self):
        self.person.delete()
        self.person_2.delete()

    @patch('app.src.serializer.serializers.PersonSerializer')
    def test_get_person(self, mock_serializer):
        mock_serializer.return_value.data = {
            'name': 'Alice Smith',
            'email': 'alice.smith@example.com'
        }

        result = self.person_logic.get_person(str(self.person.id))
        self.assertEqual(result['email'], mock_serializer.return_value.data['email'])

        with self.assertRaises(InvalidIdentifierError):
            self.person_logic.get_person('999')

    @patch('app.src.serializer.serializers.PersonSerializer')
    def test_get_person_by_email(self, mock_serializer):
        mock_serializer.return_value.data = {
            'name': 'Alice Smith',
            'email': 'alice.smith@example.com'
        }

        result = self.person_logic.get_person_by_email('alice.smith@example.com')
        self.assertEqual(result['email'], mock_serializer.return_value.data['email'])

        with self.assertRaises(InvalidIdentifierError):
            self.person_logic.get_person_by_email('nonexistent@example.com')

    @patch('app.src.serializer.serializers.PersonSerializer')
    def test_get_all_persons(self, mock_serializer):
        result = self.person_logic.get_all_persons()
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)

    @patch('app.src.serializer.serializers.PersonSerializer')
    def test_modify_person(self, mock_serializer):
        mock_serializer.return_value.is_valid.return_value = True
        mock_serializer.return_value.data = {
            'name': 'Alice Johnson',
            'email': 'alice.johnson@example.com'
        }

        updated_data = {'name': 'Alice Johnson', 'email': 'alice.johnson@example.com'}
        result = self.person_logic.modify_person(str(self.person.id), updated_data)
        self.assertEqual(result['email'], mock_serializer.return_value.data['email'])

        with self.assertRaises(InvalidIdentifierError):
            self.person_logic.modify_person('999', updated_data)

    @patch('app.src.serializer.serializers.PersonSerializer')
    def test_delete_person(self, mock_serializer):
        self.person_logic.delete_person(str(self.person.id))
        with self.assertRaises(Person.DoesNotExist):
            Person.objects.get(id=self.person.id)

        with self.assertRaises(InvalidIdentifierError):
            self.person_logic.delete_person('999')

    @patch('app.src.serializer.serializers.PersonSerializer')
    def test_create_person(self, mock_serializer):
        mock_serializer.return_value.is_valid.return_value = True

        new_person_data = {
            'name': 'Charlie Brown',
            'email': 'charlie.brown@example.com'
        }

        result = self.person_logic.create_person(new_person_data)
        self.assertEqual(result['email'], new_person_data['email'])
        person = Person.objects.get(email=new_person_data['email'])
        person.delete()

        with self.assertRaises(InvalidDataError):
            self.person_logic.create_person({'email': 'invalidemail'})


if __name__ == '__main__':
    unittest.main()