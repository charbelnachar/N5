from django.contrib.auth.hashers import make_password

from app.models import Officer
from app.src.serializer.serializers import OfficerSerializer
from app.src.exception.custom_exep import InvalidIdentifierError, InvalidDataError
from app.src.utility.util_data import UtilData
from app.src.utility.util_email import EmailValidator


class OfficerLogic:
    """
    Logic class for handling operations related to Officer.
    """

    def get_officer(self, identifier: str) -> dict:
        """
        Retrieves an officer's data based on the given identifier.

        Args:
            identifier (str): The identifier of the officer to retrieve.

        Returns:
            dict: The serialized data of the officer.

        Raises:
            InvalidIdentifierError: If the officer with the given identifier does not exist.
        """
        try:
            officer = Officer.objects.get(identifier=identifier)
        except Officer.DoesNotExist:
            raise InvalidIdentifierError(identifier, "Officer does not exist")

        serializer = OfficerSerializer(officer)
        return serializer.data

    def get_all_officers(self) -> list:
        """
        Retrieves the data of all officers.

        Returns:
            list: A list of serialized data of all officers.
        """
        officers = Officer.objects.all()
        serializer = OfficerSerializer(officers, many=True)
        return serializer.data

    def modify_officer(self, identifier: str, data: dict) -> dict:
        """
        Modifies the data of a specific officer.

        Args:
            identifier (str): The identifier of the officer to modify.
            data (dict): The data to update the officer with. It can include 'name',
                'identifier', 'username', 'email', and 'password' fields.

        Returns:
            dict: The serialized data of the updated officer.

        Raises:
            ValueError: If the officer with the given identifier does not exist.
        """



        try:
            officer = Officer.objects.get(identifier=identifier)
        except Officer.DoesNotExist:
            raise ValueError(f"Officer with identifier '{identifier}' does not exist")

        serializer = OfficerSerializer(officer, data=data)

        if serializer.is_valid():
            serializer.save()
            return serializer.data
        else:
            print(serializer.errors)
            error_message = next(iter(serializer.errors.values()))[0]
            raise InvalidDataError(data, error_message)

        return serializer.data
        #

    def delete_officer(self, identifier: str) -> None:
        """
        Deletes a specific officer.

        Args:
            identifier (str): The identifier of the officer to delete.

        Returns:
            None

        Raises:
            InvalidIdentifierError: If the officer with the given identifier does not exist.
        """
        try:
            officer = Officer.objects.get(identifier=identifier)
            user = officer.user
            user.delete()
            officer.delete()
        except Officer.DoesNotExist:
            raise InvalidIdentifierError(identifier, "Officer does not exist")
        return None

    def create_officer(self, data: dict) -> dict:
        """
        Creates a new officer.

        Args:
            data (dict): The data to create the officer with.

        Returns:
            dict: The serialized data of the created officer.

        Raises:
            InvalidDataError: If the provided data is invalid.
        """
        UtilData.validate_dict_values(data)
        EmailValidator.validate_email_format(data.get('email'))
        serializer = OfficerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        else:
            error_message = next(iter(serializer.errors.values()))[0]
            raise InvalidDataError(data, error_message)
