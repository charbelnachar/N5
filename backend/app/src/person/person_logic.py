from app.models import Person
from app.src.serializer.serializers import PersonSerializer
from app.src.exception.custom_exep import InvalidIdentifierError, InvalidDataError
from app.src.utility.util_data import UtilData
from app.src.utility.util_email import EmailValidator


class PersonLogic:
    """
    Logic class for handling operations related to Person.
    """

    def get_person(self, identifier: str) -> dict:
        """
        Retrieves a person's data based on the given identifier.

        Args:
            identifier (str): The identifier of the person to retrieve.

        Returns:
            dict: The serialized data of the person.

        Raises:
            InvalidIdentifierError: If the person with the given identifier does not exist.
        """

        try:
            person = Person.objects.get(id=identifier)
        except Person.DoesNotExist:
            raise InvalidIdentifierError(identifier, "Person does not exist")

        serializer = PersonSerializer(person)
        return serializer.data

    def get_person_by_email(self, email: str) -> dict:
        """
        Retrieves a person's data based on the given email.

        Args:
            email (str): The email of the person to retrieve.

        Returns:
            dict: The serialized data of the person.

        Raises:
            InvalidIdentifierError: If the person with the given email does not exist.
        """
        EmailValidator.validate_email_format(email)
        try:
            person = Person.objects.get(email=email)
        except Person.DoesNotExist:
            raise InvalidIdentifierError(email, "No existe usuario con este correo")

        serializer = PersonSerializer(person)
        return serializer.data


    def get_all_persons(self) -> list:
        """
        Retrieves the data of all persons.

        Returns:
            list: A list of serialized data of all persons.
        """
        persons = Person.objects.all()
        serializer = PersonSerializer(persons, many=True)
        return serializer.data

    def modify_person(self, identifier: str, data: dict) -> dict:
        """
        Modifies the data of a specific person.

        Args:
            identifier (str): The identifier of the person to modify.
            data (dict): The data to update the person with.

        Returns:
            dict: The serialized data of the updated person.

        Raises:
            InvalidIdentifierError: If the person with the given identifier does not exist.
        """
        UtilData.validate_dict_values(data)
        EmailValidator.validate_email_format(data.get('email'))
        try:
            person = Person.objects.get(id=identifier)
        except Person.DoesNotExist:
            raise InvalidIdentifierError(identifier, "Person does not exist")
        serializer = PersonSerializer(person, data=data)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        else:
            raise InvalidIdentifierError(identifier, "Person does not exist")

    def delete_person(self, identifier: str) -> None:
        """
        Deletes a specific person.

        Args:
            identifier (str): The identifier of the person to delete.

        Returns:
            None

        Raises:
            InvalidIdentifierError: If the person with the given identifier does not exist.
        """
        try:
            person = Person.objects.get(id=identifier)
            person.delete()
        except Person.DoesNotExist:
            raise InvalidIdentifierError(identifier, "Person does not exist")
        return None

    def create_person(self, data: dict) -> dict:
        """
        Creates a new person.

        Args:
            data (dict): The data to create the person with.

        Returns:
            dict: The serialized data of the created person.

        Raises:
            InvalidDataError: If the provided data is invalid.
        """
        UtilData.validate_dict_values(data)
        EmailValidator.validate_email_format(data.get('email'))
        serializer = PersonSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        else:
            print(serializer.errors)
            raise InvalidDataError(data, "invalid data provided")
